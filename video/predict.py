import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def predict_cucumber(model, img_path, threshold=0.75):
    """
    Predict whether an image contains a cucumber or not.

    Args:
    - model (tensorflow.keras.Model): The trained model.
    - img_path (str): Path to the image to be classified.
    - threshold (float): Confidence threshold for classification. Default is 0.5.

    Returns:
    - str: 'cucumber' if confidence >= threshold, otherwise 'not cucumber'.
    """

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
