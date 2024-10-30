import cv2
import numpy as np
import ffmpeg

# 동영상 파일 읽기
input_video_path = '/home/jaejun/Videos/test2.mp4'  # 원본 동영상 파일 경로
output_video_path = '/home/jaejun/camera/rawcompr/raw/test2_raw.avi'  # 저장할 동영상 파일 경로


# OpenCV로 동영상 파일 열기
cap = cv2.VideoCapture(input_video_path)

# 동영상의 프레임 너비, 높이, 초당 프레임 수 가져오기
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# ffmpeg에서 입력 스트림을 설정
process = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(frame_width, frame_height), r=fps)
    .output(output_video_path, vcodec='rawvideo', pix_fmt='bgr24', r=fps)
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

# 동영상의 각 프레임을 읽고 그대로 ffmpeg로 전달
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임을 ffmpeg 프로세스로 전달
    process.stdin.write(frame.tobytes())

# 리소스 해제
cap.release()
process.stdin.close()
process.wait()

print(f"압축 없이 동영상 저장 완료: {output_video_path}")
