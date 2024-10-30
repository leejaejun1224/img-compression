import subprocess


def remux_to_mkv(input_video, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c', 'copy', 
        output_video
    ]
    subprocess.run(command, check=True)


remux_to_mkv(
    '/home/jaejun/Videos/raw/test2_raw.avi',
    '/home/jaejun/Videos/raw/test2_raw.mkv'
)
