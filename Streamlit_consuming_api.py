import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Streamlit UI Configuration
# -----------------------------

# Custom CSS with modern design system
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main Container Styles */
    .main {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #0F172A !important;
    }
    
    /* Container styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #F8FAFC;
    }
    
    /* Card-like container for content */
    .content-container {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #1D4ED8 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 1rem;
        border: 2px dashed #CBD5E1;
        border-radius: 8px;
        background-color: #F8FAFC;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #2563EB;
        background-color: #EFF6FF;
    }
    
    /* Progress and loading indicators */
    .stProgress > div > div {
        background-color: #2563EB !important;
    }
    
    /* Text area styling */
    .stTextArea > div > div {
        border-radius: 8px;
        border-color: #CBD5E1;
    }
    
    /* Success message styling */
    .success-message {
        padding: 1rem;
        background-color: #DCFCE7;
        color: #166534;
        border-radius: 8px;
        border-left: 4px solid #22C55E;
    }
    
    /* Error message styling */
    .error-message {
        padding: 1rem;
        background-color: #FEE2E2;
        color: #991B1B;
        border-radius: 8px;
        border-left: 4px solid #EF4444;
    }
    
    /* Download button styling */
    .download-button {
        background-color: #2563EB;
        color: white !important;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none !important;
        display: inline-block;
        margin: 10px 0;
        font-weight: 500;
        text-align: center;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .download-button:hover {
        background-color: #1D4ED8;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .download-button:active {
        transform: translateY(0px);
    }
    
    /* Audio player styling */
    .stAudio > div {
        border-radius: 8px;
        background-color: #F8FAFC;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Audio Transcription & Insights", page_icon="🎧", layout="centered")

# Add logo at the top left
logo_path = r"C:\Users\ACER\Desktop\Audio To Insights\FMH New logo 24.png"
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_path, width=150)
with col2:
    st.title("🎧 Audio Transcription & Insights")
    
st.markdown("Upload an audio file, get transcription & summary, and download Excel insights.")

# API endpoint
API_URL = "https://audiotoinsights-fastapi.onrender.com/process_audio"
BASE_URL = "https://audiotoinsights-fastapi.onrender.com"

# Main content container
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# File upload section
st.subheader("📁 Upload Audio File")
st.markdown("Support formats: WAV, MP3, M4A")
uploaded_file = st.file_uploader("", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    # Display file info
    file_details = {
        "Filename": uploaded_file.name,
        "File size": f"{uploaded_file.size / 1024:.2f} KB",
        "Upload time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create two columns for file details and audio player
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### File Details")
        for key, value in file_details.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### Audio Preview")
        st.audio(uploaded_file, format="audio/wav")

    # Process button with enhanced styling
    if st.button("🎯 Process Audio", help="Click to start processing the audio file"):
        with st.spinner("🔄 Processing your audio file... Please wait..."):
            try:
                # Send audio file to FastAPI
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(API_URL, files=files)

                if response.status_code == 200:
                    data = response.json()

                    # Display Malayalam transcription with timestamps
                    transcription_text = data.get("transcription", "")
                    if transcription_text:
                        st.subheader("🗣️ Malayalam Transcript with Timestamps")
                        st.text_area("", value=transcription_text, height=300, key="transcription_area")

                    # Display summary
                    summary_text = data.get("summary", "")
                    if summary_text:
                        st.subheader("📝 Conversation Summary")
                        st.text_area("", value=summary_text, height=200, key="summary_area")

                    # Provide download link for Excel
                    download_url = data.get("download_url")
                    if download_url:
                        full_download_url = f"{BASE_URL}{download_url}"
                        st.markdown("""
                            <style>
                            .download-button {
                                background-color: #00308F;
                                color: white !important;
                                padding: 12px 24px;
                                border-radius: 8px;
                                text-decoration: none !important;
                                display: inline-block;
                                margin: 10px 0;
                                font-weight: bold;
                                text-align: center;
                                transition: background-color 0.3s;
                            }
                            .download-button:hover {
                                background-color: #004BB9;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                        st.markdown(f'<a href="{full_download_url}" class="download-button">📥 Download Excel Insights</a>', unsafe_allow_html=True)
                    else:
                        st.warning("No download URL returned from API.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
