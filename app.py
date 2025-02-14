from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS import kare
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # CORS enable kare

# Environment Variables
API_KEY = os.getenv('JBVYR', 'YTJBV')  # Default value 'YTJBV' agar environment variable set nahi hai

@app.route('/')
def home():
    return "Welcome to YouTube Video Downloader! Use /download?url=YOUTUBE_URL to download videos."

@app.route('/download', methods=['GET'])
def download_video():
    # Get video URL from query parameters
    video_url = request.args.get('url')
    
    # Check if API key is valid
    user_api_key = request.args.get('api_key')
    if user_api_key != API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key'
        }), 403

    try:
        # yt-dlp options
        ydl_opts = {
    'format': 'best',
    'quiet': True,
    'cookiefile': 'cookies.txt',  # Cookies file ka path
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.youtube.com/',  # Referer header set kare
    }
}

        # Download video info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info['url']  # Direct download URL

        # Return the download URL as JSON response
        return jsonify({
            'status': 'success',
            'download_url': download_url
        })
    except Exception as e:
        # Handle errors
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
