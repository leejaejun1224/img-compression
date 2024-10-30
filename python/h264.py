import subprocess

def compress_video_lossless(input_video, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '0',
        '-c:a', 'copy',
        output_video
    ]
    subprocess.run(command, check=True)

# 사용 예시
compress_video_lossless('/home/jaejun/camera/rawcompr/raw/test2_raw.avi', '/home/jaejun/camera/rawcompr/results/test2_raw_compressed.mkv')
