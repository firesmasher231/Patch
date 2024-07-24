import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

class ImageClassifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Classifier and Renamer")

        self.current_image_pair = []
        self.image_index = 0
        self.pair_index = 1
        self.target_dir = ""
        self.has_trimming = None

        # Setup GUI elements
        self.image_frame = tk.Frame(root)
        self.image_frame.pack()

        self.image_label_1 = tk.Label(self.image_frame, bg="lightblue")
        self.image_label_1.grid(row=0, column=0)

        self.image_label_2 = tk.Label(self.image_frame, bg="lightgreen")
        self.image_label_2.grid(row=0, column=1)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.load_images_button = tk.Button(root, text="Load Images", command=self.load_images)
        self.load_images_button.pack()

        self.select_target_button = tk.Button(root, text="Select Target Directory", command=self.select_target_directory)
        self.select_target_button.pack()

        self.before_button_1 = tk.Button(self.button_frame, text="1: Before (Left)", command=lambda: self.classify_image(0, "before"))
        self.before_button_1.grid(row=0, column=0)

        self.before_button_2 = tk.Button(self.button_frame, text="2: Before (Right)", command=lambda: self.classify_image(1, "before"))
        self.before_button_2.grid(row=0, column=1)

        self.cut_button = tk.Button(self.button_frame, text="3: Cut", command=lambda: self.set_trimming(True))
        self.cut_button.grid(row=1, column=0)

        self.uncut_button = tk.Button(self.button_frame, text="4: Uncut", command=lambda: self.set_trimming(False))
        self.uncut_button.grid(row=1, column=1)

        self.skip_button = tk.Button(root, text="Space: Skip", command=self.skip)
        self.skip_button.pack()

        self.generate_val_button = tk.Button(root, text="Generate Validation Set", command=self.generate_validation_set)
        self.generate_val_button.pack()

        self.root.bind('1', lambda event: self.classify_image(0, "before"))
        self.root.bind('2', lambda event: self.classify_image(1, "before"))
        self.root.bind('3', lambda event: self.set_trimming(True))
        self.root.bind('4', lambda event: self.set_trimming(False))
        self.root.bind('<space>', lambda event: self.skip())

    def load_images(self):
        self.image_dir = filedialog.askdirectory(title="Select Directory with Images")
        if self.image_dir:
            self.images = sorted([img for img in os.listdir(self.image_dir) if img.endswith(('jpg', 'jpeg', 'png'))])
            self.show_image_pair()

    def select_target_directory(self):
        self.target_dir = filedialog.askdirectory(title="Select Target Directory")

    def show_image_pair(self):
        if self.image_index < len(self.images) - 1:
            self.current_image_pair = [self.images[self.image_index], self.images[self.image_index + 1]]
            self.display_images()
        else:
            messagebox.showinfo("Info", "No more images to display")

    def display_images(self):
        img1 = Image.open(os.path.join(self.image_dir, self.current_image_pair[0]))
        img2 = Image.open(os.path.join(self.image_dir, self.current_image_pair[1]))

        img1 = img1.resize((400, 400), Image.LANCZOS)
        img2 = img2.resize((400, 400), Image.LANCZOS)

        img1 = ImageTk.PhotoImage(img1)
        img2 = ImageTk.PhotoImage(img2)

        self.image_label_1.configure(image=img1)
        self.image_label_1.image = img1

        self.image_label_2.configure(image=img2)
        self.image_label_2.image = img2

    def set_trimming(self, has_trimming):
        self.has_trimming = has_trimming

    def classify_image(self, image_index, label):
        if self.has_trimming is not None and self.target_dir:
            after_index = 1 if image_index == 0 else 0
            trimming_label = 'cut' if self.has_trimming else 'uncut'
            self.copy_images(image_index, after_index, trimming_label)
            self.has_trimming = None
            self.image_index += 2  # Move to the next pair
            self.show_image_pair()
        else:
            messagebox.showwarning("Warning", "Please specify whether the images are cut or uncut")

    def skip(self):
        self.image_index += 1  # Skip one image and keep the other
        self.show_image_pair()

    def copy_images(self, before_index, after_index, trimming_label):
        before_img = self.current_image_pair[before_index]
        after_img = self.current_image_pair[after_index]

        before_new_name = f"img{self.pair_index}_before.jpg"
        after_new_name = f"img{self.pair_index}_after.jpg"

        train_before_dir = os.path.join(self.target_dir, 'train', trimming_label, 'before')
        train_after_dir = os.path.join(self.target_dir, 'train', trimming_label, 'after')

        os.makedirs(train_before_dir, exist_ok=True)
        os.makedirs(train_after_dir, exist_ok=True)

        shutil.copy(os.path.join(self.image_dir, before_img), os.path.join(train_before_dir, before_new_name))
        shutil.copy(os.path.join(self.image_dir, after_img), os.path.join(train_after_dir, after_new_name))
        
        self.pair_index += 1

    def generate_validation_set(self):
        for trimming_label in ['cut', 'uncut']:
            train_before_dir = os.path.join(self.target_dir, 'train', trimming_label, 'before')
            train_after_dir = os.path.join(self.target_dir, 'train', trimming_label, 'after')
            val_before_dir = os.path.join(self.target_dir, 'validation', trimming_label, 'before')
            val_after_dir = os.path.join(self.target_dir, 'validation', trimming_label, 'after')

            os.makedirs(val_before_dir, exist_ok=True)
            os.makedirs(val_after_dir, exist_ok=True)

            before_images = os.listdir(train_before_dir)
            after_images = os.listdir(train_after_dir)

            total_pairs = len(before_images)
            val_size = int(0.2 * total_pairs)
            val_indices = random.sample(range(total_pairs), val_size)

            for idx in val_indices:
                before_image = before_images[idx]
                after_image = after_images[idx]

                shutil.move(os.path.join(train_before_dir, before_image), os.path.join(val_before_dir, before_image))
                shutil.move(os.path.join(train_after_dir, after_image), os.path.join(val_after_dir, after_image))

        messagebox.showinfo("Info", "Validation set generated successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClassifier(root)
    root.mainloop()
