import asyncio
import functools
import inspect
import io
import logging
import math
from hashlib import md5
from os import SEEK_END
from pathlib import PurePath

from pyrogram import Client, StopTransmission, raw

LOGGER = logging.getLogger(__name__)


class TelegramClient(Client):
    """KuriGram client with a configurable upload request pipeline."""

    def __init__(self, *args, upload_workers=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.upload_workers = max(1, upload_workers)

    async def save_file(
        self, path, file_id=None, file_part=0, progress=None, progress_args=()
    ):
        """Upload a file using more in-flight parts than KuriGram's fixed four."""
        async with self.save_file_semaphore:
            if path is None:
                return None

            async def worker(session, queue):
                while data := await queue.get():
                    try:
                        await session.invoke(data)
                    except Exception as exc:
                        LOGGER.exception(exc)

            part_size = 512 * 1024
            if isinstance(path, (str, PurePath)):
                fp = open(path, "rb")  # noqa: ASYNC230
            elif isinstance(path, io.IOBase):
                fp = path
            else:
                raise ValueError(
                    "Invalid file. Expected a file path or a binary file pointer"
                )

            try:
                file_name = getattr(fp, "name", "file.jpg")
                fp.seek(0, SEEK_END)
                file_size = fp.tell()
                fp.seek(0)
                if file_size == 0:
                    raise ValueError("File size equals to 0 B")

                file_size_limit_mib = 4000 if self.me and self.me.is_premium else 2000
                if file_size > file_size_limit_mib * 1024 * 1024:
                    raise ValueError(
                        f"Can't upload files bigger than {file_size_limit_mib} MiB"
                    )

                file_total_parts = math.ceil(file_size / part_size)
                is_big = file_size > 10 * 1024 * 1024
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None
                session = await self.get_session(
                    await self.storage.dc_id(), is_media=True
                )
                queue = asyncio.Queue(self.upload_workers)
                workers = [
                    self.loop.create_task(worker(session, queue))
                    for _ in range(self.upload_workers if is_big else 1)
                ]

                fp.seek(part_size * file_part)
                while chunk := fp.read(part_size):
                    rpc = (
                        raw.functions.upload.SaveBigFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            file_total_parts=file_total_parts,
                            bytes=chunk,
                        )
                        if is_big
                        else raw.functions.upload.SaveFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            bytes=chunk,
                        )
                    )
                    await queue.put(rpc)
                    if is_missing_part:
                        return None
                    if md5_sum:
                        md5_sum.update(chunk)
                    file_part += 1
                    if progress:
                        callback = functools.partial(
                            progress,
                            min(file_part * part_size, file_size),
                            *progress_args,
                        )
                        if inspect.iscoroutinefunction(progress):
                            await callback()
                        else:
                            await self.loop.run_in_executor(self.executor, callback)

                for _ in workers:
                    await queue.put(None)
                await asyncio.gather(*workers)
                if is_big:
                    return raw.types.InputFileBig(
                        id=file_id, parts=file_total_parts, name=file_name
                    )
                return raw.types.InputFile(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,
                    md5_checksum="".join(
                        f"{value:02x}" for value in md5_sum.digest()
                    ),
                )
            except StopTransmission:
                raise
            finally:
                if isinstance(path, (str, PurePath)):
                    fp.close()
