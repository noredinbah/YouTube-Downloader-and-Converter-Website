from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def convert_to_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error converting video to audio: {e}")
        return None

def download_youtube_video(link, quality):
    try:
        video = YouTube(link)
        stream = video.streams.filter(res=quality).first()
        if stream:
            return stream.download()
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
    return None

def download_youtube_audio(link):
    try:
        video = YouTube(link)
        audio = video.streams.filter(only_audio=True).first()
        if audio:
            return audio.download()
    except Exception as e:
        print(f"Error downloading YouTube audio: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    choice = request.form.get('choice')
    filepath = None
    message = "Invalid choice"

    if choice == '1':
        link = request.form.get('link')
        quality = request.form.get('quality')
        filepath = download_youtube_video(link, quality)
        message = "Video downloaded successfully" if filepath else "Failed to download video. Check the link or quality."

    elif choice == '2':
        linkaudio = request.form.get('linkaudio')
        filepath = download_youtube_audio(linkaudio)
        message = "Audio downloaded successfully" if filepath else "Failed to download audio. Check the link."

    elif choice == '3':
        file = request.files.get('file')
        if file and file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            pathaudio = convert_to_audio(file_path, f"{file_path}.mp3")
            filepath = pathaudio
            message = "Audio converted successfully" if filepath else "Failed to convert video to audio."
        else:
            message = "No file selected or invalid file."

    return render_template('result.html', message=message, filepath=filepath)

@app.route('/download/<path:filepath>', methods=['GET'])
def download(filepath):
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
    
#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)