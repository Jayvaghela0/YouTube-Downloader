from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Environment Variables
API_KEY = os.getenv('JBVYR', 'YTJBV')

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
            'format': 'best',  # Best quality
            'quiet': True,     # Suppress logs
            'outtmpl': 'video.mp4',  # Video file ka naam
            'cookiefile': 'cookies.txt',  # Cookies file ka path
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
            }
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Video file ka path
        video_path = 'video.mp4'

        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Video downloaded successfully',
            'video_url': f'/serve_video?path={video_path}'
        })
    except Exception as e:
        # Handle errors
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/serve_video', methods=['GET'])
def serve_video():
    # Get video file path from query parameters
    video_path = request.args.get('path')
    
    # Serve video file
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
