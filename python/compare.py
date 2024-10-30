import cv2
import numpy as np

def compare_videos(video1_path, video2_path):
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    frame_index = 0
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 and not ret2:
            print("비디오 끝에 도달했습니다. 두 비디오는 동일합니다.")
            break
        if not ret1 or not ret2:
            print("두 비디오의 프레임 수가 다릅니다.")
            break

        if not np.array_equal(frame1, frame2):
            print(f"프레임 {frame_index}에서 차이가 있습니다.")
            break

        frame_index += 1

    cap1.release()
    cap2.release()

# 사용 예시
compare_videos('/home/jaejun/camera/rawcompr/raw/test2_raw.avi', '/home/jaejun/camera/rawcompr/results/test2_raw_compressed.mkv')
