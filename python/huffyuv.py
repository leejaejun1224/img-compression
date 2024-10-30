import subprocess

def compress_video_lossless_huffyuv(input_video, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'huffyuv',  
        '-c:a', 'copy',    
        output_video
    ]
    subprocess.run(command, check=True)
