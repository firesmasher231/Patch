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

# Custom preprocessing function to convert grayscale to RGB
def preprocess_grayscale_to_rgb(image):
    image = tf.image.grayscale_to_rgb(image)  # Convert grayscale to RGB
    return preprocess_input(image)

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    # preprocessing_function=preprocess_input,
    preprocessing_function=preprocess_grayscale_to_rgb,
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
    color_mode="grayscale",
)

val_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    color_mode="grayscale",
)

# Load the VGG16 model without the top layers
base_model = VGG16(
    weights="imagenet", include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
)

# Freeze the base model
for layer in base_model.layers:
    layer.trainable = False

# Add new top layers for our classification task
x = Flatten()(base_model.output)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(3, activation="softmax")(
    x
)  # 3 classes: well maintained, partially maintained, overgrown


model = Model(inputs=base_model.input, outputs=output)


# Compile the model
model.compile(
    optimizer=Adam(learning_rate=0.0001),  # changed from 0.0001
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# Train the model
history = model.fit(train_generator, epochs=10, validation_data=val_generator)

# Unfreeze some layers of the base model for fine-tuning
for layer in base_model.layers[-4:]:
    layer.trainable = True

# Recompile the model with a lower learning rate
model.compile(
    optimizer=Adam(learning_rate=0.00001),  # from 0.00001
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# Continue training the model
history_fine = model.fit(train_generator, epochs=10, validation_data=val_generator)

# Save the fine-tuned model
model.save("hedge_classifier_vgg16.h5")

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

# Load the model
model = load_model("hedge_classifier_vgg16.h5")

# Load and preprocess a new image
image_path = "test2.jpg"
image = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
image = img_to_array(image)
image = preprocess_input(image)
image = np.expand_dims(image, axis=0)

# Predict the class
predictions = model.predict(image)
print(predictions)
class_indices = train_generator.class_indices
class_labels = {v: k for k, v in class_indices.items()}
predicted_class = class_labels[np.argmax(predictions)]

print(f"The image is classified as: {predicted_class}")
