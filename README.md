# YouTube Transcript Downloader

A simple and robust tool to download transcripts from YouTube videos. It comes with a **beautiful, interactive web interface** built with Streamlit, and a **command-line script** for batch processing.

## Features

- **Beautiful Web Interface**: Paste a YouTube URL or video ID into the web app, fetch the transcript with auto-translation if needed, preview it, and copy or download it instantly.
- **Smart Language Selection**: Automatically attempts to fetch the English transcript. If an English transcript isn't available, it falls back to the default language and translates it to English.
- **Auto-Naming**: Fetches the video's title using YouTube's oEmbed API to name the saved transcript file cleanly.
- **Docker Support**: Easily run the web application in an isolated container without installing dependencies locally.
- **Command-Line Batching**: Support for single URLs, multiple URLs, or reading from a `.txt` file via the original CLI script.

---

## 🌐 Running the Web Application

The easiest way to use the downloader is via the interactive Streamlit web application.

### Option 1: Running with Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t youtube-transcript-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 youtube-transcript-app
   ```
3. Open your browser and navigate to `http://localhost:8501`.

### Option 2: Running Locally via Python

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Streamlit server:
   ```bash
   python3 -m streamlit run app.py
   ```

---

## 💻 Running the Command Line Script (`main.py`)

If you prefer the terminal or want to batch-download multiple transcripts, you can use the original script (`main.py`).

### Prerequisites
Make sure you have installed dependencies via `pip install -r requirements.txt`.

### Usage Methods

#### 1. Hardcoded URL (Quickest Method)
Edit `main.py` and paste your YouTube URL into the `VIDEO_URL` variable at the top of the file:
```python
# ==========================================
# PASTE YOUR YOUTUBE URL HERE
# ==========================================
VIDEO_URL = "https://www.youtube.com/watch?v=..."
```
Then run the script:
```bash
python3 main.py
```
*Note: Ensure `VIDEO_URL` is set to an empty string `""` if you want to use the methods below.*

#### 2. Command Line Arguments
You can pass one or more YouTube URLs directly via the command line:
```bash
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID_1" "https://www.youtube.com/watch?v=VIDEO_ID_2"
```

#### 3. Read from a Text File
Create a text file (e.g., `urls.txt`) with one YouTube URL per line, then pass the file to the script:
```bash
python3 main.py urls.txt
```
