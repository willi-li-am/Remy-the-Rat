import cv2
from video import capture_video_feed
from train_model import create_and_train_model
from predict import predict_cucumber

def main():
    # load and train model
    train_dir = 'dataset/train'
    validation_dir = 'dataset/validation'
    model = create_and_train_model(train_dir, validation_dir, epochs=10)

    # capture video feed
    # Open connection to camera (1 is droidcam)
    # note KEEP the droidcam app ON otherwise 
    camera = cv2.VideoCapture(1)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the resulting frame
        cv2.imshow('Camera Feed', frame)

        # Check for user input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Save the current frame to a file
            snapshot_path = 'snapshot.jpg'
            cv2.imwrite(snapshot_path, frame)
            print(f"Snapshot saved to {snapshot_path}")

            # Predict if the snapshot contains a cucumber
            predict_cucumber(model, snapshot_path, threshold=0.75)

    # Release the camera and close all OpenCV windows
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
