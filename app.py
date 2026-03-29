import streamlit as st
import yt_dlp
import os
import io
import static_ffmpeg
static_ffmpeg.add_paths()

# Set Page Config
st.set_page_config(
    page_title="YT Video/Audio Downloader",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 YouTube Video/Audio Downloader")
st.markdown("Download your favorite YouTube videos in your preferred quality or extract audio as MP3.")

# Input URL
url = st.text_input("🔗 Paste YouTube Video URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # 1. Fetch Video Metadata first (without downloading)
        with st.spinner("Fetching video information..."):
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                title = info.get('title', 'Unknown Title')
                thumbnail = info.get('thumbnail')
                duration = info.get('duration') # in seconds
                views = info.get('view_count')

        # 2. Display Video Info
        st.success("Video Found!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if thumbnail:
                st.image(thumbnail)
        with col2:
            st.subheader(title)
            if duration:
                st.write(f"⏱️ **Duration:** {duration // 60}m {duration % 60}s")
            if views:
                st.write(f"👀 **Views:** {views:,}")

        st.divider()

        # 3. Download Options
        st.subheader("📥 Download Options")
        
        format_type = st.radio("Select Format:", ["Video", "Audio (MP3)"])

        quality_choice = None
        # Video Resolution selection
        if format_type == "Video":
            quality_choice = st.selectbox(
                "Choose Resolution (Height):", 
                ["Best Quality Available", "1080p", "720p", "480p", "360p"]
            )

        if st.button("Generate Download Link"):
            with st.spinner("Processing download... This may take a minute for high resolutions."):
                
                # Create a downloads folder if it doesn't exist
                if not os.path.exists("downloads"):
                    os.makedirs("downloads")

                outtmpl = "downloads/%(title)s.%(ext)s"

                # Setup yt-dlp options based on choice
                if format_type == "Video":
                    mime_type = "video/mp4"
                    file_extension = "mp4"

                    # Map UI choices to yt-dlp height filters
                    if quality_choice == "Best Quality Available":
                        # Downloads the best available MP4 video merging it with best audio
                        res_filter = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                    else:
                        # Extracts the height number (e.g., '1080p' -> '1080')
                        height = quality_choice.replace("p", "")
                        # Filters for resolutions less than or equal to chosen height
                        res_filter = f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

                    ydl_opts = {
                        'format': res_filter,
                        'outtmpl': outtmpl,
                        'merge_output_format': 'mp4', # Forces merging into MP4
                    }

                else:
                    # Audio (MP3) Options
                    mime_type = "audio/mp3"
                    file_extension = "mp3"
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': outtmpl,
                    }

                # Download file to local server storage
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info_dict)
                    
                    # yt-dlp may change output name after postprocessing, let's capture it
                    if format_type == "Audio (MP3)":
                        file_path = os.path.splitext(file_path)[0] + ".mp3"
                    elif format_type == "Video" and not file_path.endswith(".mp4"):
                         file_path = os.path.splitext(file_path)[0] + ".mp4"

                # Read the file into memory to give it to Streamlit download button
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()

                    st.success("✅ File processed successfully!")
                    
                    # Provide download button
                    st.download_button(
                        label=f"💾 Click here to download {file_extension.upper()}",
                        data=file_bytes,
                        file_name=f"{title}.{file_extension}",
                        mime=mime_type
                    )

                    # Delete file from local server storage to save space
                    os.remove(file_path)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("Built with Python, yt-dlp & Streamlit 🚀")