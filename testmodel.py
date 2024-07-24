from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Load the model
model = load_model("hedge_classifier_vgg16.h5")

# Load and preprocess a new image
image_path = "test.jpg"
image = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
image = img_to_array(image)
image = preprocess_input(image)
image = np.expand_dims(image, axis=0)

# Predict the class
predictions = model.predict(image)
class_indices = train_generator.class_indices
class_labels = {v: k for k, v in class_indices.items()}
predicted_class = class_labels[np.argmax(predictions)]

print(f"The image is classified as: {predicted_class}")
