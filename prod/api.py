from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import io
from tensorflow.keras.applications.vgg16 import preprocess_input

# Initialize the Flask application
app = Flask(__name__)

# Load the model
model = load_model("hedge_classifier_vgg16.h5")

# Define image dimensions
IMG_HEIGHT = 224
IMG_WIDTH = 224


# Route to handle image prediction
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No image selected for uploading"}), 400

    if file:
        # Read the file contents into a BytesIO object
        image_bytes = file.read()
        image = io.BytesIO(image_bytes)

        # Load and preprocess the image
        image = load_img(image, target_size=(IMG_HEIGHT, IMG_WIDTH))
        # Convert the image to grayscale
        # image = image.convert("L")

        image = img_to_array(image)
        image = preprocess_input(image)
        image = np.expand_dims(image, axis=0)

        # Predict the class
        predictions = model.predict(image)
        class_indices = {
            "overgrown": 0,
            "partiallymaintained": 1,
            "wellmaintained": 2,
        }  # Update this as per your training class labels
        class_labels = {v: k for k, v in class_indices.items()}
        predicted_class = class_labels[np.argmax(predictions)]

        return jsonify(
            {"predictions": predictions.tolist(), "predicted_class": predicted_class}
        )

    return jsonify({"error": "Something went wrong"}), 500


if __name__ == "__main__":
    app.run(debug=True)
