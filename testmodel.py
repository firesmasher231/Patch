
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

# Set the paths
base_dir = "labeled_images"  # Path to your labeled dataset
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")

# Image dimensions
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    color_mode="grayscale"
)

val_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    # color_mode="grayscale"
)

# Load the model
model = load_model("hedge_classifier_vgg16.h5")
# Load and preprocess new images
# image_paths = ["test.jpg", "test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg", "test5.jpg"]
image_paths = ["305paper/wellmaintained.jpg", "305paper/partiallymaintained.jpg", "305paper/overgrown.jpg"]
for image_path in image_paths:
    image = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    # Preprocess the image into grayscale
    image = image.convert("L")

    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    # Predict the class
    predictions = model.predict(image)
    class_indices = train_generator.class_indices
    class_labels = {v: k for k, v in class_indices.items()}
    predicted_class = class_labels[np.argmax(predictions)]
    print(predictions)
    print(f"The image {image_path} is classified as: {predicted_class}")
