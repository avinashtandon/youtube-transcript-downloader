# YouTube Transcript Downloader

A simple and robust Python script to download transcripts from YouTube videos and save them as plain text files. The script automatically fetches the video title and uses it as the filename.

## Features

- **Multiple Input Methods**:
  - Hardcode a URL in the script (`VIDEO_URL` variable).
  - Pass single or multiple URLs as command-line arguments.
  - Pass a `.txt` file containing a list of URLs (one per line).
- **Smart Language Selection**: Automatically attempts to fetch the English transcript. If an English transcript isn't available, it falls back to the default language and translates it to English.
- **Auto-Naming**: Fetches the video's title using YouTube's oEmbed API to name the saved transcript file cleanly.
- **Clean Output**: Saves transcripts as readable plain text files.
- **Warning Suppression**: Suppresses irrelevant OpenSSL warnings from underlying libraries for a cleaner console output.

## Prerequisites

You will need Python 3 installed and the following Python packages:

```bash
pip3 install youtube-transcript-api requests
```

## Usage

### 1. Hardcoded URL (Quickest Method)
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

*Note: The script prioritizes the hardcoded `VIDEO_URL`. If you want to use the command-line methods below, ensure `VIDEO_URL` is set to an empty string `""`.*

### 2. Command Line Arguments
You can pass one or more YouTube URLs directly via the command line:
```bash
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID_1" "https://www.youtube.com/watch?v=VIDEO_ID_2"
```

### 3. Read from a Text File
Create a text file (e.g., `urls.txt`) with one YouTube URL per line, then pass the file to the script:
```bash
python3 main.py urls.txt
```

## Output

The script will generate a `.txt` file for each successfully processed video in the same directory as the script. The filename will match the video's title (e.g., `My Video Title.txt`).
