import subprocess
import os

def download_and_convert_audio(url, target_file, return_value):
    ytdl = subprocess.Popen(["youtube-dl", url, "-f", "bestaudio", "-o", target_file],
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE)

    try:
        ytdl.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        output, errors = ytdl.communicate()
        with open("ytdl_errors.txt","w") as f:
            f.write(output)
            f.write("\n\n==========\n\n")
            f.write(errors)
        ytdl.kill()
        return_value.append("youtube-dl timeout")
        return

    """ffmpeg = subprocess.Popen(["ffmpeg", "-nostdin", "-vn", "-i", target_file, "-sample_fmt", "s16", "-ar", "48000", target_file + ".wav"],
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE)

    try:
        ffmpeg.communicate(timeout=20)
        os.unlink(target_file)
    except subprocess.TimeoutExpired:
        output, errors = ffmpeg.communicate()
        with open("ffmpeg_errors.txt", "w") as f:
            f.write(output)
            f.write("\n\n==============\n\n")
            f.write(errors)
        ffmpeg.kill()
        return_value.append("ffmpeg timeout")
        os.unlink(target_file)
        return"""

    return_value.append(True)
