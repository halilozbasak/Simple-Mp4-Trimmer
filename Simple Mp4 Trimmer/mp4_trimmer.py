import os
import subprocess
from moviepy.editor import VideoFileClip

def parse_time(time_str):
    if ':' in time_str:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    else:
        return float(time_str)

def trim_mp4_moviepy(input_file, output_file, start_time, end_time):
    try:
        start_seconds = parse_time(start_time)
        end_seconds = parse_time(end_time)
        
        with VideoFileClip(input_file) as video:
            trimmed_video = video.subclip(start_seconds, end_seconds)
            trimmed_video.write_videofile(output_file, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, preset='ultrafast')
        return f"Trimmed video saved as {output_file}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def trim_mp4_ffmpeg(input_file, output_file, start_time, end_time):
    try:
        start_seconds = parse_time(start_time)
        end_seconds = parse_time(end_time)
        duration = end_seconds - start_seconds
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-ss', str(start_seconds),
            '-t', str(duration),
            '-c', 'copy',
            output_file
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f"Trimmed video saved as {output_file}"
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr.decode()}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def trim_mp4(input_file, output_dir, start_time, end_time, method='ffmpeg'):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(input_file).split('.')[0] + '_trimmed.mp4')
    
    if method == 'moviepy':
        return trim_mp4_moviepy(input_file, output_file, start_time, end_time)
    elif method == 'ffmpeg':
        return trim_mp4_ffmpeg(input_file, output_file, start_time, end_time)
    else:
        return "Invalid method specified. Use 'moviepy' or 'ffmpeg'."
