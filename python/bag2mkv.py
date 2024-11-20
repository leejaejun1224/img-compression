import rosbag
import cv2
from cv_bridge import CvBridge
import os
import subprocess

# 설정
rosbag_file = '/home/jaejun/bagfile/1120/test1.bag'  # 입력 rosbag 파일 경로
output_video = '/home/jaejun/Videos/raw/test1.mkv'  # 출력 동영상 파일 경로
topic_name = '/usb_cam/image_raw'  # 읽을 토픽 이름
frame_rate = 5  # 출력 동영상의 프레임 레이트 (필요에 따라 조정)
output_dir = 'frames'  # 프레임을 저장할 디렉토리


def save_frames_from_rosbag(bag_file, output_dir, topic):
    """
    ROS bag 파일에서 프레임을 읽어 디렉토리에 저장
    """
    bridge = CvBridge()
    bag = rosbag.Bag(bag_file, 'r')
    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    for _, msg, _ in bag.read_messages(topics=[topic]):
        try:
            # ROS Image 메시지를 OpenCV 형식으로 변환
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            frame_path = os.path.join(output_dir, f"frame_{frame_count:05d}.bmp")
            cv2.imwrite(frame_path, cv_image)
            frame_count += 1
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")

    bag.close()
    print(f"Saved {frame_count} frames to {output_dir}")
    return frame_count

def create_mkv_with_ffmpeg(output_dir, output_video, frame_rate):
    """
    저장된 프레임을 사용해 MKV 포맷으로 동영상 생성
    """
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # 기존 파일 덮어쓰기
        "-framerate", str(frame_rate),
        "-i", os.path.join(output_dir, "frame_%05d.bmp"),
        "-c:v", "rawvideo",  # 무압축 저장
        "-pix_fmt", "bgr24",  # 픽셀 포맷
        "-an",  # 오디오 스트림 제거
        "-allow_raw_vfw", "1",  # Matroska의 VFW 모드 활성화
        output_video
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Uncompressed MKV video saved as {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating MKV: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg and try again.")
    os.remove(output_dir)


frame_count = save_frames_from_rosbag(rosbag_file, output_dir, topic_name)
if frame_count > 0:
    create_mkv_with_ffmpeg(output_dir, output_video, frame_rate)
