import argparse
from pytube import YouTube
import youtube_dl
import os

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download videos as MP4 or MP3.")
    parser.add_argument("url", type=str, help="The URL of the video to download.")
    parser.add_argument("--output", type=str, default=".", help="The directory where the video will be saved (default: current directory).")
    parser.add_argument("--format", type=str, choices=['mp4', 'mp3'], default="mp4", help="The format to download (default: mp4).")
    parser.add_argument("--source", type=str, choices=['youtube', 'other'], default="youtube", help="The source of the video (default: youtube).")

    args = parser.parse_args()

    if args.source == "youtube":
        downloaded_file = download_youtube_video(args.url, args.output, args.format)
    else:
        download_video(args.url, args.output, args.format)
    
    print(f"Video downloaded to: {args.output}")
