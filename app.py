from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Media Grabber API is running!"

@app.route('/api/grab', methods=['POST'])
def grab_media():
    data = request.get_json()
    url = data.get('url') if data else None

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'video')

            return jsonify({
                'success': True,
                'title': title,
                'download_url': video_url
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
