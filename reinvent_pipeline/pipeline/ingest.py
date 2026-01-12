import os
import glob
import yt_dlp

def download_captions(url, output_dir="/app/output"):
    """
    Downloads captions (subtitles) for a YouTube video and returns the VTT file path.
    Automatically handles language codes in the file name.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'skip_download': True,            # don't download video
        'writesubtitles': True,           # download subtitles
        'writeautomaticsub': True,        # fallback to automatic subtitles
        'subtitlesformat': 'vtt',         # force VTT
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s')  # video ID based filename
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # Find the actual VTT file (may include language code like .en.vtt)
    files = glob.glob(os.path.join(output_dir, f"{info['id']}*.vtt"))
    if not files:
        raise FileNotFoundError(f"No VTT file found for video {url}")
    
    return files[0]   # return first matching file
