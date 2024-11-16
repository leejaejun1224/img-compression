import subprocess
import hashlib
import os
import tempfile
import shutil
import time

def extract_frames(video_path, output_dir, pix_fmt):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vsync', '0',
        '-f', 'rawvideo',
        '-pix_fmt', pix_fmt,  # 지정된 픽셀 포맷 사용
        os.path.join(output_dir, 'frame_%08d.raw')
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def hash_frames(frame_dir):
    hashes = []
    frame_files = sorted(os.listdir(frame_dir))
    total_size = 0
    for frame_file in frame_files:
        file_path = os.path.join(frame_dir, frame_file)
        with open(file_path, 'rb') as f:
            data = f.read()
            total_size += len(data)
            hashes.append(hashlib.md5(data).hexdigest())
    return hashes, total_size

def check_lossless_by_frames(input_video, compressed_video, pix_fmt='yuv444p'):
    temp_dir1 = tempfile.mkdtemp()
    temp_dir2 = tempfile.mkdtemp()

    try:
        # 입력 및 압축된 비디오의 크기 확인
        input_video_size = os.path.getsize(input_video)
        compressed_video_size = os.path.getsize(compressed_video)

        print("입력 비디오에서 프레임 추출 중...")
        start_time = time.time()
        extract_frames(input_video, temp_dir1, pix_fmt)
        input_extract_time = time.time() - start_time

        print("압축된 비디오에서 프레임 추출 중...")
        start_time = time.time()
        extract_frames(compressed_video, temp_dir2, pix_fmt)
        compressed_extract_time = time.time() - start_time

        print("프레임의 해시 값 계산 중...")
        hashes1, total_size1 = hash_frames(temp_dir1)
        hashes2, total_size2 = hash_frames(temp_dir2)

        # 압축률 계산
        compression_ratio = (compressed_video_size / input_video_size) * 100

        # 초당 압축 속도 계산 (MB/s)
        total_time = input_extract_time + compressed_extract_time
        total_data_processed = (total_size1 + total_size2) / (1024 * 1024)  # 바이트를 MB로 변환
        compression_speed = total_data_processed / total_time

        if hashes1 == hashes2:
            print("영상은 프레임 수준에서 동일합니다. 무손실 압축이 완료되었습니다.")
        else:
            print("영상은 프레임 수준에서 차이가 있습니다. 손실이 발생했습니다.")

        print(f"압축률: {compression_ratio:.2f}%")
        print(f"초당 압축 속도: {compression_speed:.2f} MB/s")

    finally:
        shutil.rmtree(temp_dir1)
        shutil.rmtree(temp_dir2)
