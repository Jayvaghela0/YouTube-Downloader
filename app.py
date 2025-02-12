from flask import Flask, request, jsonify
import youtube_downloader
import os

app = Flask(__name__)

# Environment variables se API key aur secret fetch karein
API_KEY = os.getenv("JBVYT", "default_key")  # Agar environment variable nahi mila, to "default_key" use hoga
API_SECRET = os.getenv("YTJBV", "default_secret")  # Agar environment variable nahi mila, to "default_secret" use hoga

@app.route('/download', methods=['GET'])
def download_video():
    # API key aur secret ko verify karein
    provided_key = request.args.get('key')
    provided_secret = request.args.get('secret')

    if provided_key != API_KEY or provided_secret != API_SECRET:
        return jsonify({"error": "Unauthorized access"}), 401

    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', None)

    return jsonify({
        "status": "success",
        "title": video_title,
        "ext": video_ext
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
