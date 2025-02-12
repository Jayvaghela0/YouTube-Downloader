from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    download_url = stream.url
    return jsonify({'download_url': download_url})

if __name__ == '__main__':
    app.run(debug=True)
