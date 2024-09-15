import cv2
import threading
import queue
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

class VideoPlayer:
    def __init__(self):
        self.is_running = True
        self.playback_queue = queue.Queue()
        self.playback_thread = threading.Thread(target=self._video_worker, daemon=True)
        self.playback_thread.start()

    def _video_worker(self):
        # get the pre-trained ML model
        model_path = 'E:/Remy-the-Rat/video/cucumber_classifier.keras' 
        self.model = load_model(model_path)

        # capture video feed
        # Open connection to camera (1 is droidcam)
        # note KEEP the droidcam app ON otherwise 
        self.camera = cv2.VideoCapture(1)
        if not self.camera.isOpened():
            print("Error: Could not open camera.")
            return
        while self.is_running:
            # Capture frame-by-frame
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Display the resulting frame
            cv2.imshow('Camera Feed', frame)

            # Check for user input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break

        # Release the camera and close all OpenCV windows
        self.camera.release()
        cv2.destroyAllWindows()

    def capture_frame_as_base64(self):
        if self.is_running:
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read frame.")
                return
            
            # Save frame to jpg, convert it to base64 and return it
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = buffer.tobytes()
            
            # Encode the bytes to base64
            base64_encoded = base64.b64encode(image_data)
            base64_string = base64_encoded.decode('utf-8')
            return base64_string


    def predict_frame(self, frame):
         # Save the current frame to a file
        snapshot_path = 'snapshot.jpg'
        cv2.imwrite(snapshot_path, frame)
        # Predict if the snapshot contains a cucumber
        self.predict_cucumber(self.model, snapshot_path)


    def predict_cucumber(self, model, img_path, threshold=0.6):
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = tf.expand_dims(img_array, 0)  # Add batch dimension

        # Make prediction
        prediction = model.predict(img_array)
        confidence = prediction[0][0]

        # Determine label based on confidence threshold
        if confidence >= threshold:
            print('cucumber! confidence: ' + str(confidence))
            return 'cucumber'
        else:
            print('non_cucumber! confidence:' + str(confidence))
            return 'non_cucumber'

    def stop(self):
        self.is_running = False
        self.playback_thread.join()  # Ensure thread finishes