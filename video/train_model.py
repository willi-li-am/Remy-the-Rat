import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def create_and_train_model(train_dir, validation_dir, epochs=10):
    """
    Creates, trains, and returns a model for detecting cucumbers vs non-cucumbers.

    Args:
    - train_dir (str): Path to the training dataset directory.
    - validation_dir (str): Path to the validation dataset directory.
    - epochs (int): Number of epochs for training. Default is 10.
    - threshold (float): Confidence threshold for classification. Default is 0.5.

    Returns:
    - model (tensorflow.keras.Model): The trained model.
    """
    # Data augmentation and preprocessing
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    validation_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
    )

    # Training generator
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',  # Binary classification
        color_mode='rgb',
        shuffle=True,
        classes=['non_cucumber', 'cucumber']
    )

    # Validation generator
    validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',  # Binary classification
        color_mode='rgb',
        shuffle=True,
        classes=['non_cucumber', 'cucumber']
    )

    print("Train class indices:", train_generator.class_indices)
    print("Validation class indices:", validation_generator.class_indices)

    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=x)

    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )

    # Save the trained model
    model.save('cucumber_classifier.keras')
    return model
