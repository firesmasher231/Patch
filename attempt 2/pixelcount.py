import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

# Load DeepLab model from TensorFlow Hub
model_url = "https://tfhub.dev/tensorflow/deeplabv3/1"
model = hub.load(model_url)

def preprocess_image_for_model(image_path):
    # Read image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize image to fit model input requirements
    input_image = tf.image.resize(image, (513, 513))
    input_image = tf.cast(input_image, tf.float32) / 127.5 - 1
    input_image = tf.expand_dims(input_image, axis=0)
    
    return input_image, image

def get_segmentation_mask(image):
    # Predict segmentation mask
    predictions = model(image)
    predictions = tf.argmax(predictions["semantic"], axis=-1)
    predictions = tf.squeeze(predictions, axis=0)
    
    return predictions.numpy()

def count_hedge_pixels(mask):
    # Assuming hedges are classified as "plant" in the PASCAL VOC dataset
    # In the PASCAL VOC dataset, the "plant" class is labeled as 17
    hedge_pixels = np.sum(mask == 17)
    
    return hedge_pixels

# Define image paths
before_img_path = os.path.join( 'img2_before.jpg')
after_img_path = os.path.join( 'img2_after.jpg')

# Load and preprocess images
before_input, before_image = preprocess_image_for_model(before_img_path)
after_input, after_image = preprocess_image_for_model(after_img_path)

# Get segmentation masks
before_mask = get_segmentation_mask(before_input)
after_mask = get_segmentation_mask(after_input)

# Count hedge pixels
before_hedge_pixels = count_hedge_pixels(before_mask)
after_hedge_pixels = count_hedge_pixels(after_mask)

# Calculate the difference in hedge pixels
difference_in_hedge_pixels = after_hedge_pixels - before_hedge_pixels

# Display the results
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('Before')
plt.imshow(before_image)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('After')
plt.imshow(after_image)
plt.axis('off')

plt.tight_layout()
plt.show()

(before_hedge_pixels, after_hedge_pixels, difference_in_hedge_pixels)