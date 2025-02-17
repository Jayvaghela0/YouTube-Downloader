from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yt_dlp
import time
import threading
import undetected_chromedriver as uc  # Web player method ke liye

app = Flask(__name__)
CORS(app)

# Environment Variables (Render ke env variables se fetch ho raha hai)
API_KEY = os.getenv("YTJBV")  # API Key
ENV_VALUE = os.getenv("JBVYT")  # Extra environment variable

# Video download folder
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# yt-dlp custom path (agar manually install kiya hai)
YTDLP_PATH = "./yt-dlp"  # Ensure yt-dlp binary is in the project folder

# Function to delete video after 2 minutes
def delete_video_after_delay(video_path, delay=120):
    time.sleep(delay)
    if os.path.exists(video_path):
        os.remove(video_path)

# Extract video stream URL using Selenium
def get_video_stream_url(video_url):
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    try:
        driver.get(video_url)
        time.sleep(5)  # Wait for page to load
        video_element = driver.find_element("tag name", "video")
        stream_url = video_element.get_attribute("src")
        return stream_url
    except Exception as e:
        return str(e)
    finally:
        driver.quit()

@app.route('/') 
def home(): 
    return "Welcome to YouTube Downloader! Use/download? URL=YOUTUBE_URL to download videos. "
      
@app.route("/download", methods=["GET"])
def download_video():
    video_url = request.args.get("url")
    api_key = request.args.get("api_key")  # API key validate karne ke liye

    # Check if API Key matches
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    if not video_url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Get the streaming URL
        stream_url = get_video_stream_url(video_url)

        # yt-dlp options with custom binary path
        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "postprocessor_args": ["--no-warnings"],
            "youtube_dl": YTDLP_PATH,  # Custom yt-dlp binary
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(stream_url, download=True)
            video_filename = ydl.prepare_filename(info_dict)
            video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

            # Delete video after 2 minutes
            threading.Thread(target=delete_video_after_delay, args=(video_path, 120)).start()

            return jsonify({"download_link": f"/downloads/{video_filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
