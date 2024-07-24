image_path = "img.jpg"

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the image
# image_path = '/mnt/data/x_____x3Fy3lvhWoyB1uNqDslnUMA..x_____x_ags_d4179754-4826-11ef-89b9-1228a0b974d3.jpg'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, 40, 50)

# Display the results
plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image)
plt.subplot(1, 2, 2)
plt.title("Edges")
plt.imshow(edges, cmap='gray')
plt.show()

# Reshape the image for clustering
pixels = image.reshape((-1, 3))
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(pixels)

# Convert the result to an image
segmented_image = kmeans.cluster_centers_[kmeans.labels_]
segmented_image = segmented_image.reshape(image.shape).astype(np.uint8)

# Display the segmented image
plt.figure(figsize=(10, 10))
plt.title("Segmented Image")
plt.imshow(segmented_image)
plt.show()

# Extract features from the segmented image
def extract_features(image, segments):
    features = []
    labels = []
    for (i, segVal) in enumerate(np.unique(segments)):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        mask[segments == segVal] = 255
        hist = cv2.calcHist([image], [0, 1, 2], mask, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        features.append(hist)
        labels.append(segVal)
    return np.array(features), np.array(labels)

segments = kmeans.labels_.reshape(image.shape[:2])
features, labels = extract_features(image, segments)

# Display the segmented image with unique labels
plt.figure(figsize=(10, 10))
plt.title("Segmented Image with Labels")
plt.imshow(segments, cmap='jet')
plt.show()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the classifier
accuracy = clf.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Predict the segments in the image
predicted_labels = clf.predict(features)

# Check if the size matches
if predicted_labels.size != image.shape[0] * image.shape[1]:
    raise ValueError("The number of predicted labels does not match the image size.")

# Reshape the predicted labels to match the image shape
predicted_segments = predicted_labels.reshape(image.shape[:2])

# Apply morphological operations to refine the edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
refined_edges = cv2.morphologyEx(predicted_segments.astype(np.uint8), cv2.MORPH_CLOSE, kernel)

# Display the final result
plt.figure(figsize=(10, 10))
plt.title("Refined Edges")
plt.imshow(refined_edges, cmap='gray')
plt.show()
