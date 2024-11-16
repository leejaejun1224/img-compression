import subprocess

def save_uncompressed_mkv(input_mkv, output_mkv):
    """
    MKV 파일을 무압축으로 저장하고 색상 반전 문제 해결
    """
    command = [
        "ffmpeg",
        "-i", input_mkv,            # 입력 파일
        "-c:v", "rawvideo",         # 비디오를 무압축으로 저장
        "-pix_fmt", "bgr24",        # 픽셀 포맷을 BGR로 지정
        "-an",                      # 오디오 스트림 제거
        "-allow_raw_vfw", "1",      # VFW 모드 활성화
        output_mkv                  # 출력 파일
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully saved uncompressed MKV with corrected colors as {output_mkv}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg and try again.")
# 사용 예제
input_mkv = "/home/jaejun/Videos/raw/sample_1920x1080.mkv"      # 원본 MKV 파일 경로
output_mkv = "/home/jaejun/Videos/raw/sample_1920x1080_raw.mkv"    # 무압축으로 저장할 MKV 파일 경로

save_uncompressed_mkv(input_mkv, output_mkv)
