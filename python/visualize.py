import cv2

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break  

        cv2.imshow('Decoding', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# play_video('/home/jaejun/Videos/results/test2_raw_compressed.avi')
