import streamlit as st
import re
import warnings
import requests

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
    # If the user just inputted the 11 character ID
    if len(url) == 11 and re.match(r'^[0-9A-Za-z_-]{11}$', url):
        return url
    return None

def get_video_title(video_id):
    try:
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

st.set_page_config(page_title="YouTube Transcript Downloader", page_icon="🎥", layout="centered")

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main container centering and padding */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    /* Title styling */
    h1 {
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: #FF0000;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* stHorizontalBlock alignment */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    /* Button styling */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        border-radius: 10px !important;
        font-weight: 600 !important;
        height: 48px !important;
        min-height: 48px !important;
        margin: 0 !important;
        transition: all 0.3s ease;
    }
    /* Input box styling */
    .stTextInput > div > div > input {
        height: 48px;
        border-radius: 10px;
    }
    /* Primary Fetch Button */
    .stButton > button[kind="primary"] {
        background-color: #FF0000;
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #cc0000;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
    }
    /* Text area */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }
    /* Hide menus */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🎥 YouTube Transcript Downloader")
st.markdown("<div class='subtitle'>Quickly fetch and download transcripts from any YouTube video</div>", unsafe_allow_html=True)

st.write("---")

# Initialize session state for storing transcript between reruns
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "title" not in st.session_state:
    st.session_state.title = None
if "output_file" not in st.session_state:
    st.session_state.output_file = None

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    url_input = st.text_input("YouTube Video URL or ID:", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

with col2:
    fetch_clicked = st.button("Fetch Transcript", type="primary")

if fetch_clicked:
    if url_input:
        video_id = extract_video_id(url_input)
        if not video_id:
            st.error(f"Error: Could not extract video ID from input: {url_input}")
        else:
            with st.spinner(f"Fetching transcript for video ID: {video_id}..."):
                title = get_video_title(video_id)
                st.session_state.title = title
                st.session_state.output_file = f"{title}.txt"
                
                try:
                    transcript_list = YouTubeTranscriptApi().list(video_id)
                    
                    try:
                        transcript_obj = transcript_list.find_transcript(['en'])
                        st.info(f"Found English transcript (Auto-generated: {transcript_obj.is_generated})")
                    except Exception:
                        transcript_obj = next(iter(transcript_list))
                        st.info(f"English not available. Using transcript in: {transcript_obj.language} (Auto-generated: {transcript_obj.is_generated})")
                        
                        if 'en' in transcript_obj.translation_languages:
                            st.info("Translating transcript to English...")
                            transcript_obj = transcript_obj.translate('en')
                    
                    transcript = transcript_obj.fetch()
                    formatter = TextFormatter()
                    st.session_state.transcript = formatter.format_transcript(transcript)
                    st.success(f"Transcript fetched successfully! Title: **{title}**")
                    
                except Exception as e:
                    st.error(f"An error occurred while fetching the transcript: {e}")
    else:
        st.warning("Please enter a YouTube URL or Video ID.")

# Display from session state so it persists when clicking 'Download'
if st.session_state.transcript:
    st.text_area(
        "Transcript Preview",
        st.session_state.transcript,
        height=450
    )

    st.markdown("<br>", unsafe_allow_html=True)

    import html
    import streamlit.components.v1 as components

    escaped_text = html.escape(st.session_state.transcript)
    filename = html.escape(st.session_state.output_file)

    components.html(
        f"""
        <style>
            .button-container {{
                display: flex;
                gap: 1rem;
                width: 100%;
            }}
            .custom-btn {{
                flex: 1;
                height: 48px;
                border-radius: 10px;
                border: 1px solid rgba(49, 51, 63, 0.2);
                background: white;
                color: #31333F;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.25s ease;
                font-family: 'Inter', sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .custom-btn:hover {{
                border-color: #FF0000;
                color: #FF0000;
            }}
        </style>

        <textarea id="text-data" style="display:none;">{escaped_text}</textarea>

        <div class="button-container">
            <button class="custom-btn" onclick="downloadText()">⬇️ Download Transcript</button>
            <button id="copy-btn" class="custom-btn" onclick="copyText()">📋 Copy Transcript</button>
        </div>

        <script>
            function copyText() {{
                const text = document.getElementById("text-data").value;
                
                // Fallback for clipboard api inside iframe
                const textArea = document.getElementById("text-data");
                textArea.style.display = "block";
                textArea.select();
                document.execCommand("copy");
                textArea.style.display = "none";

                const btn = document.getElementById("copy-btn");
                btn.innerHTML = "✅ Copied!";
                btn.style.borderColor = "#4CAF50";
                btn.style.color = "#4CAF50";

                setTimeout(() => {{
                    btn.innerHTML = "📋 Copy Transcript";
                    btn.style.borderColor = "rgba(49,51,63,0.2)";
                    btn.style.color = "#31333F";
                }}, 2000);
            }}

            function downloadText() {{
                const text = document.getElementById("text-data").value;
                const blob = new Blob([text], {{ type: 'text/plain' }});
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "{filename}";
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }}
        </script>
        """,
        height=65,
    )
