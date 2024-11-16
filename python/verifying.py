import subprocess
import hashlib
import os
import tempfile
import shutil

def extract_frames(video_path, output_dir):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vsync', '0',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        os.path.join(output_dir, 'frame_%08d.raw')
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def hash_frames(frame_dir):
    hashes = []
    frame_files = sorted(os.listdir(frame_dir))
    for frame_file in frame_files:
        with open(os.path.join(frame_dir, frame_file), 'rb') as f:
            data = f.read()
            hashes.append(hashlib.md5(data).hexdigest())
    return hashes

def check_lossless_by_frames(input_video, compressed_video):
    temp_dir1 = tempfile.mkdtemp()
    temp_dir2 = tempfile.mkdtemp()

    try:
        print("Extracting frames from input video...")
        extract_frames(input_video, temp_dir1)
        print("Extracting frames from compressed video...")
        extract_frames(compressed_video, temp_dir2)

        print("Calculating hashes of frames...")
        hashes1 = hash_frames(temp_dir1)
        hashes2 = hash_frames(temp_dir2)

        if hashes1 == hashes2:
            print("영상은 프레임 수준에서 동일합니다. 무손실 압축이 완료되었습니다.")
        else:
            print("영상은 프레임 수준에서 차이가 있습니다. 손실이 발생했습니다.")
    finally:
        shutil.rmtree(temp_dir1)
        shutil.rmtree(temp_dir2)
