import subprocess


def compress_video_lossless_h264(input_video, output_video):
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
    
    print("Compressing Succeed!")


# compress_video_lossless('/home/jaejun/Videos/raw/test2_raw.avi', '/home/jaejun/Videos/results/test2_raw_compressed.avi')
