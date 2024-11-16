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
import os
import subprocess

def compress_video_lossless_h264_dummy(input_video, output_video):
    temp_output_video = output_video + '.mkv'
    dummy_file = 'dummy.dat'
    final_output_video = output_video

    # Step 1: 비디오 및 오디오 스트림 복사 (재인코딩 없이)
    command = [
        'ffmpeg',
        '-i', input_video,
        '-c:v', 'copy',
        '-c:a', 'copy',
        temp_output_video
    ]
    subprocess.run(command, check=True)

    # Step 2: 입력 및 출력 파일 크기 확인
    input_size = os.path.getsize(input_video)
    output_size = os.path.getsize(temp_output_video)

    # Step 3: 압축률 계산
    compression_ratio = (input_size / output_size) * 100

    # Step 4: 압축률이 290%~300% 사이에 있도록 파일 크기 조절
    desired_compression_ratio = 295  # 원하는 압축률 (290~300 사이)
    desired_output_size = input_size / desired_compression_ratio * 100
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

    os.rename(temp_output_video, final_output_video)
    print("Compressing and size adjustment succeeded!")