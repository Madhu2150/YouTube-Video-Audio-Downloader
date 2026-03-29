# 🎬 YouTube Video & Audio Downloader

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive, local desktop utility built with Streamlit and Python to scrape and download YouTube media. Unlike cloud-deployed downloaders which get IP-blocked by YouTube, running this app locally uses your standard residential network to bypass blocks effortlessly! 

---

## ✨ Features

- 🔍 **Real-time Previews:** Scrapes and renders video thumbnails, durations, titles, and view counts before starting a download.
- 🎥 **Multi-Resolution Video Downloads:** Automatically merges high-quality video and audio tracks (Up to 1080p).
- 🎵 **Lossless MP3 Conversion:** Isolates media streams and writes standalone 192kbps `.mp3` files.
- ⚙️ **Automatic FFmpeg Binaries:** Leverages `static-ffmpeg` to dynamically set up environment paths without needing manual OS software installs.
- 🧹 **Automatic Caching and Wipe Cleans:** Once files are downloaded via the browser UI, server caches are immediately scrubbed to save hard disk space.

---

## 🛠️ Tech Stack

- **UI Front-end:** Streamlit
- **Scraper & Engine:** `yt-dlp`
- **Native Rendering Engine:** `static-ffmpeg`

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Madhu2150/YouTube-Video-Audio-Downloader.git
cd YouTube-Video-Audio-Downloader

### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt

### 3. Run the App
```bash
streamlit run app.py