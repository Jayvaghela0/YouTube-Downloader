from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

# Environment Variables
API_KEY = os.getenv('JBVYR', 'YTJBV')  # Default value 'YTJBV' agar environment variable set nahi hai

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
        # Create YouTube object
        yt = YouTube(video_url)
        
        # Get the highest resolution progressive stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        
        # Get the download URL
        download_url = stream.url
        
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
