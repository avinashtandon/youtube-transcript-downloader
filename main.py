import sys
import re
import os
import warnings

# ==========================================
# PASTE YOUR YOUTUBE URL HERE
# ==========================================
VIDEO_URL = "https://www.youtube.com/watch?v=KMrhBGw56LI"

# Suppress urllib3 warnings about OpenSSL
warnings.filterwarnings("ignore")

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url):
    # Extract video ID from youtube URLs (handles youtube.com and youtu.be)
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_video_title(video_id):
    try:
        import requests
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            title = response.json().get('title', video_id)
            # Clean title for filename by removing invalid characters
            clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
            return clean_title.strip()
    except Exception:
        pass
    return f"transcript_{video_id}"

def download_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Error: Could not extract video ID from URL: {url}")
        return
    
    title = get_video_title(video_id)
    output_file = f"{title}.txt"
    
    try:
        print(f"\nFetching transcript for video ID: {video_id}...")
        
        # Get the list of available transcripts
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        # Try to find an English transcript first
        try:
            transcript_obj = transcript_list.find_transcript(['en'])
            print(f"Found English transcript (Auto-generated: {transcript_obj.is_generated})")
        except Exception:
            # If English is not available, just grab the first available transcript
            transcript_obj = next(iter(transcript_list))
            print(f"English not available. Using transcript in: {transcript_obj.language} (Auto-generated: {transcript_obj.is_generated})")
            
            # Translate it to English if possible
            if 'en' in transcript_obj.translation_languages:
                print("Translating transcript to English...")
                transcript_obj = transcript_obj.translate('en')
        
        # Fetch the transcript data
        transcript = transcript_obj.fetch()
        
        # Format the transcript as plain text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_formatted)
            
        print(f"Transcript successfully saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")

if __name__ == "__main__":
    # If the user pasted a URL in the VIDEO_URL variable, use that first
    if VIDEO_URL.strip():
        download_transcript(VIDEO_URL.strip())
        
    # Otherwise, check command line arguments
    elif len(sys.argv) < 2:
        print("Usage:")
        print("  Paste your URL into the VIDEO_URL variable at the top of this script, OR run:")
        print("  python youtube_transcript_downloader.py <url_1> <url_2> ...")
        print("  python youtube_transcript_downloader.py urls.txt")
    else:
        # Check if the first argument is meant to be a file
        if sys.argv[1].endswith('.txt'):
            if os.path.isfile(sys.argv[1]):
                print(f"Reading URLs from file: {sys.argv[1]}")
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                if not urls:
                    print(f"The file {sys.argv[1]} is empty.")
                else:
                    for url in urls:
                        download_transcript(url)
            else:
                print(f"Error: The file '{sys.argv[1]}' was not found.")
                print(f"Please make sure to create '{sys.argv[1]}' in the current folder before running the script.")
        else:
            # Process all arguments as URLs
            for url in sys.argv[1:]:
                download_transcript(url)
