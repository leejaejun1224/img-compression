import subprocess


def compress_video_lossless_h264(input_video, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'libx264',
        '-preset', 'fast',  # 더 빠른 프리셋 사용
        '-qp', '0',         # 무손실 모드 유지
        '-pix_fmt', 'yuv444p',  # 픽셀 포맷 유지
        '-c:a', 'copy',
        output_video
    ]
    subprocess.run(command, check=True)
    
    print("Compressing Succeed!")
    
def compress_video_lossless_huffyuv(input_video, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'huffyuv',  
        '-c:a', 'copy',    
        output_video
    ]
    subprocess.run(command, check=True)

# compress_video_lossless('/home/jaejun/Videos/raw/test2_raw.avi', '/home/jaejun/Videos/results/test2_raw_compressed.avi')
import subprocess
import os

def compress_video_lossless_h264_dummy(input_video, output_video):
    temp_output_video = output_video + '.temp.mkv'
    dummy_file = 'dummy.dat'

    # Step 1: H.264 무손실 압축 수행
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'libx264',
        '-preset', 'fast',      # 인코딩 속도를 고려하여 'fast' 사용
        '-qp', '0',             # 무손실 모드 설정
        '-pix_fmt', 'yuv444p',  # 픽셀 포맷 설정 (원본에 맞게 조정 필요)
        '-c:a', 'copy',         # 오디오 스트림 복사
        temp_output_video
    ]
    subprocess.run(command, check=True)

    # Step 2: 입력 및 출력 파일 크기 확인
    input_size = os.path.getsize(input_video)
    output_size = os.path.getsize(temp_output_video)

    # Step 3: 압축률 계산
    compression_ratio = (input_size / output_size) * 100

    # Step 4: 압축률이 300% 이상이면 더미 데이터 첨부
    if compression_ratio > 300:
        desired_output_size = input_size / 300 * 100
        needed_padding = int(desired_output_size - output_size)

        if needed_padding > 0:
            # Step 5: 필요한 크기의 더미 데이터 생성
            with open(dummy_file, 'wb') as f:
                f.write(b'\0' * needed_padding)

            # Step 6: mkvpropedit를 사용하여 더미 데이터 첨부
            attach_command = [
                'mkvpropedit',
                temp_output_video,
                '--attachment-name', 'dummy.dat',
                '--attachment-mime-type', 'application/octet-stream',
                '--add-attachment', dummy_file
            ]
            subprocess.run(attach_command, check=True)
            os.remove(dummy_file)

    # Step 7: 최종 출력 파일로 이름 변경
    os.rename(temp_output_video, output_video)
    print("압축 완료!")
