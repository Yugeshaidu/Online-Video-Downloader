from flask import Flask, request, render_template, redirect, url_for
from pytube import YouTube
import youtube_dl
import os

app = Flask(__name__)

def download_youtube_video(url, output_path, format):
    yt = YouTube(url)
    
    if format == "mp4":
        stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
    elif format == "mp3":
        stream = yt.streams.filter(only_audio=True).first()
    
    file_path = stream.download(output_path=output_path)
    return file_path

def download_video(url, output_path, format):
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else {}
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        output_path = "downloads"
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        if 'youtube' in url:
            download_youtube_video(url, output_path, format)
        else:
            download_video(url, output_path, format)
        
        return redirect(url_for('success', format=format))
    return render_template('index.html')

@app.route('/success')
def success():
    format = request.args.get('format')
    return f"Video downloaded successfully in {format} format!"

if __name__ == "__main__":
    app.run(debug=True)
