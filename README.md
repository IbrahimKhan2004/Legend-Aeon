<h1 align="center">⚡ AEON-L3 ⚡</h1>

<p align="center">
  <b>A powerful, high-performance, feature-rich Mirror & Leech Telegram Bot.</b>
</p>

<p align="center">
  <i>An updated fork of <a href="https://github.com/AeonOrg/Aeon-MLTB">AeonOrg/Aeon-MLTB</a>.</i>
</p>

<p align="center">
  <a href="https://github.com/L3G3N7/Aeon/blob/main/LICENSE"><img src="https://img.shields.io/github/license/L3G3N7/Aeon?style=for-the-badge&color=orange" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-yellow.svg?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Supported-blue.svg?style=for-the-badge&logo=docker" alt="Docker"></a>
</p>

---

## 📑 Table of Contents
- [About AEON-L3](#-about-aeon-l3)
- [✨ Key Features](#-key-features)
- [🐳 Docker Deployment](#-docker-deployment)
  - [Method 1: Docker CLI](#method-1-docker-cli)
  - [Method 2: Docker Compose](#method-2-docker-compose)
- [☁️ Other Deployment Options](#️-other-deployment-options)
  - [Heroku Deployment](#heroku-deployment)
  - [VPS / Local Linux Machine](#vps--local-linux-machine)
- [⚙️ Configuration & Environment Variables](#️-configuration--environment-variables)
- [📖 Documentation Links](#-documentation-links)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [🙏 Acknowledgements & Credits](#-acknowledgements--credits)

---

## 🧐 About AEON-L3

**AEON-L3** is an updated fork of [AeonOrg/Aeon-MLTB](https://github.com/AeonOrg/Aeon-MLTB). It is a streamlined, optimized, and multi-functional Telegram bot built to mirror, leech, and manage files across multiple cloud services and protocols seamlessly. 

Whether you need to download direct links, torrents, NZB usenet files, YouTube videos, JDownloader packages, or Telegram files, AEON-L3 handles them all and uploads them straight to **Google Drive**, **Rclone remotes**, or **Telegram Cloud**.

---

## ✨ Key Features

- **Multi-Source Support:** Download from Direct Links, Torrents (qBittorrent/Aria2), Usenet (SABnzbd), YouTube-DLP, JDownloader, Mega, and Telegram files.
- **Multiple Destination Uploads:** Upload directly to Google Drive, Rclone Remotes, or Telegram Cloud (Leech).
- **Speed & Optimization:** Powered by `uv` Python package manager and containerized with Docker for ultra-fast performance.
- **Advanced File Management:** Zip/Unzip, split files, custom captions, thumbnail selection, file renaming, metadata editing, and video watermarking.
- **Force Subscribe & Paid Channels:** Built-in membership checks, token verification system, and channel access control.
- **RSS & Multi-User Management:** Integrated RSS feed monitoring, user authorization, sudo access, and task queues.

---

## 🐳 Docker Deployment

Deploying AEON-L3 via **Docker** is the recommended method for production environments as it guarantees isolation, reproducibility, and minimal dependency overhead.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your server/system.
- [Docker Compose](https://docs.docker.com/compose/install/) (optional but recommended).

---

### Method 1: Docker CLI

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/L3G3N7/Aeon.git
   cd Aeon
   ```

2. **Configure Environment Variables:**
   Copy the sample configuration file and update it with your credentials:
   ```bash
   cp config_sample.py config.py
   ```
   *Edit `config.py` using `nano` or `vim` to set required variables like `BOT_TOKEN`, `OWNER_ID`, `TELEGRAM_API`, `TELEGRAM_HASH`, and `DATABASE_URL`.*

3. **Build the Docker Image:**
   ```bash
   docker build -t aeon-l3 .
   ```

4. **Run the Docker Container:**
   ```bash
   docker run -d \
     --name aeon-l3-bot \
     --restart always \
     --net=host \
     aeon-l3
   ```

5. **Check Container Logs:**
   ```bash
   docker logs -f aeon-l3-bot
   ```

---

### Method 2: Docker Compose

For easier management, a pre-configured `docker-compose.yml` is already included in the repository. Configuration variables are loaded directly from `config.py`.

1. **Clone the Repository & Setup Configuration:**
   ```bash
   git clone https://github.com/L3G3N7/Aeon.git
   cd Aeon
   cp config_sample.py config.py
   ```
   *Edit `config.py` with your credentials.*

2. **Start the Service:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop or View Logs:**
   ```bash
   # View logs
   docker-compose logs -f

   # Stop bot
   docker-compose down
   ```

---

## ☁️ Other Deployment Options

<details>
<summary><b>Click to expand Heroku Deployment Instructions</b></summary>

### Heroku Deployment

1. **Fork and Star** this repository.
2. Go to repository **Settings** -> **Actions** and enable GitHub Actions.
3. Open the **Actions** tab and select the **Deploy to Heroku** workflow.
4. Click **Run workflow** and fill in the required environment variables:
   - `BOT_TOKEN`, `OWNER_ID`, `DATABASE_URL`, `TELEGRAM_API`, `TELEGRAM_HASH`, `HEROKU_APP_NAME`, `HEROKU_EMAIL`, `HEROKU_API_KEY`.
5. Trigger the workflow and wait for deployment completion.
</details>

<details>
<summary><b>Click to expand VPS / Local Linux Machine Deployment</b></summary>

### VPS / Local Linux Machine

1. **Update System & Install Dependencies:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip git ffmpeg aria2 qbittorrent-nox -y
   ```

2. **Clone Repository & Setup Virtual Environment:**
   ```bash
   git clone https://github.com/L3G3N7/Aeon.git
   cd Aeon
   python3 -m venv venv
   source venv/bin/activate
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Configure & Start Bot:**
   ```bash
   cp config_sample.py config.py
   # Edit config.py with your credentials
   bash start.sh
   ```
</details>

---

## ⚙️ Configuration & Environment Variables

| Variable | Type | Required | Description |
| :--- | :---: | :---: | :--- |
| `BOT_TOKEN` | `str` | **Yes** | Telegram Bot Token obtained from [@BotFather](https://t.me/BotFather). |
| `OWNER_ID` | `int` | **Yes** | Telegram User ID of the bot owner. |
| `TELEGRAM_API` | `int` | **Yes** | Telegram API ID from [my.telegram.org](https://my.telegram.org). |
| `TELEGRAM_HASH` | `str` | **Yes** | Telegram API Hash from [my.telegram.org](https://my.telegram.org). |
| `DATABASE_URL` | `str` | Optional | MongoDB Connection URL for saving user settings, RSS feeds, and bot states. |
| `GDRIVE_ID` | `str` | Optional | Google Drive Folder/TeamDrive ID or `root`. |
| `RCLONE_PATH` | `str` | Optional | Default Rclone remote path (e.g., `remote:folder`). |
| `AUTHORIZED_CHATS` | `str` | Optional | Space-separated list of authorized chat/group IDs. |
| `SUDO_USERS` | `str` | Optional | Space-separated list of user IDs given sudo access. |
| `LEECH_DUMP_CHAT` | `str` | Optional | Chat or Channel ID where leeched files are dumped. |

*For a full list of configuration options, check out the [Configurations Guide](docs/CONFIGURATIONS.md).*

---

## 📖 Documentation Links

- 🚀 [Deployment Guide](docs/DEPLOYMENT.md)
- ⚙️ [Configuration Options](docs/CONFIGURATIONS.md)
- ✨ [Feature Details](docs/FEATURES.md)
- 🤖 [Bot Commands](docs/COMMANDS.md)
- 🛠️ [Extra Tools & Scripts](docs/EXTRAS.md)

---

## 🤝 Contributing

Contributions are always welcome! If you want to contribute:
1. Fork the project repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements & Credits

- **AEON-L3** is an updated fork of [AeonOrg/Aeon-MLTB](https://github.com/AeonOrg/Aeon-MLTB).
- Special thanks to the original creators of [Mirror-Leech-Telegram-Bot](https://github.com/anasty17/mirror-leech-telegram-bot).
- Gratitude to all open-source developers whose tools and libraries made this project possible.

<p align="center">
  Updated with ❤️ by <a href="https://github.com/L3G3N7">L3G3N7</a>
</p>
