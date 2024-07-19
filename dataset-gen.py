import os
import shutil
import random

# Define project base directory (adjust as needed)
project_base_dir = os.path.abspath(os.path.dirname(__file__))

# Paths
dataset_path = os.path.join(project_base_dir, 'raw')
train_before_dir = os.path.join(project_base_dir, 'dataset/train/before')
train_after_dir = os.path.join(project_base_dir, 'dataset/train/after')
val_before_dir = os.path.join(project_base_dir, 'dataset/validation/before')
val_after_dir = os.path.join(project_base_dir, 'dataset/validation/after')

# Create directories if they do not exist
os.makedirs(train_before_dir, exist_ok=True)
os.makedirs(train_after_dir, exist_ok=True)
os.makedirs(val_before_dir, exist_ok=True)
os.makedirs(val_after_dir, exist_ok=True)

# Parameters
validation_split = 0.2  # 20% for validation

# Get all image names
images = os.listdir(dataset_path)

# Group images by pairs
paired_images = {}
for image in images:
    if 'before' in image:
        pair_id = image.split('_before')[0]
    elif 'after' in image:
        pair_id = image.split('_after')[0]
    if pair_id not in paired_images:
        paired_images[pair_id] = []
    paired_images[pair_id].append(image)

# Split pairs into training and validation sets
pair_ids = list(paired_images.keys())
random.shuffle(pair_ids)
split_index = int(len(pair_ids) * (1 - validation_split))
train_pairs = pair_ids[:split_index]
val_pairs = pair_ids[split_index:]

# Function to move files to the respective directories
def move_files(pairs, source_dir, dest_before_dir, dest_after_dir):
    for pair_id in pairs:
        for image in paired_images[pair_id]:
            if 'before' in image:
                shutil.move(os.path.join(source_dir, image), os.path.join(dest_before_dir, image))
            elif 'after' in image:
                shutil.move(os.path.join(source_dir, image), os.path.join(dest_after_dir, image))

# Move training files
move_files(train_pairs, dataset_path, train_before_dir, train_after_dir)

# Move validation files
move_files(val_pairs, dataset_path, val_before_dir, val_after_dir)

print("Dataset split into training and validation sets successfully!")
