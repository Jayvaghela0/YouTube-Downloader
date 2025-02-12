from flask import Flask, request, jsonify
import youtube_dl

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
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
