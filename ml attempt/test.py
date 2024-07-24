import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import cv2

# Load the trained model
model = tf.keras.models.load_model("model/hedge_cutting_detector.keras")


# Function to preprocess images
def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize to [0, 1]
    return img_array


# Paths to the pair of images to test
image_before_path = os.path.join("dataset", "test", "img7_before.jpg")
image_after_path = os.path.join("dataset", "test", "img7_after.jpg")

# Preprocess the images
image_before = preprocess_image(image_before_path)
image_after = preprocess_image(image_after_path)

# Predict using the model
prediction_before = model.predict(image_before)[0][0]
prediction_after = model.predict(image_after)[0][0]

# Print the predictions
print(f"Prediction for 'before' image: {'Cut' if prediction_before > 0.5 else 'Uncut'}")
print(f"Prediction for 'after' image: {'Cut' if prediction_after > 0.5 else 'Uncut'}")


# Function to display the images with predictions
def display_images_with_predictions(before_path, after_path, pred_before, pred_after):
    img_before = cv2.imread(before_path)
    img_after = cv2.imread(after_path)

    label_before = "Cut" if pred_before > 0.5 else "Uncut"
    label_after = "Cut" if pred_after > 0.5 else "Uncut"

    cv2.putText(
        img_before,
        f"Prediction: {label_before}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        img_after,
        f"Prediction: {label_after}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    combined_image = np.hstack((img_before, img_after))
    cv2.imshow("Before and After with Predictions", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Display the images with predictions
display_images_with_predictions(
    image_before_path, image_after_path, prediction_before, prediction_after
)
