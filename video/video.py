import cv2

def capture_video_feed():
    # Open connection to camera (1 is droidcam)
    # note KEEP the droidcam app ON otherwise 
    camera = cv2.VideoCapture(1)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # capture frame-by-frame
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the resulting frame
        cv2.imshow('Camera Feed', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video_feed()
