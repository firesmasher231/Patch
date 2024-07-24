import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class CropTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crop Tool")
        
        self.image_dir = ""
        self.images = []
        self.image_index = 0
        self.current_image = None
        self.current_image_path = ""
        self.crop_box = None
        self.rect = None
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.is_cropping = False

        # GUI elements
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        
        self.load_button = tk.Button(root, text="Load Images", command=self.load_images)
        self.load_button.pack()

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.do_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)
        self.root.bind("<space>", self.save_crop)

    def load_images(self):
        self.image_dir = filedialog.askdirectory(title="Select Directory with Images")
        if self.image_dir:
            self.images = sorted([img for img in os.listdir(self.image_dir) if img.endswith(('jpg', 'jpeg', 'png'))])
            self.show_image()

    def show_image(self):
        if self.image_index < len(self.images):
            self.current_image_path = os.path.join(self.image_dir, self.images[self.image_index])
            self.current_image = Image.open(self.current_image_path)
            self.display_image()
        else:
            messagebox.showinfo("Info", "No more images to display")

    def display_image(self):
        self.canvas.delete("all")
        img = self.current_image.resize((800, 800), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def start_crop(self, event):
        self.is_cropping = True
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def do_crop(self, event):
        if self.is_cropping:
            self.end_x, self.end_y = event.x, event.y
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def end_crop(self, event):
        self.is_cropping = False
        self.end_x, self.end_y = event.x, event.y
        self.crop_box = (self.start_x, self.start_y, self.end_x, self.end_y)

    def save_crop(self, event):
        if self.crop_box:
            left, top, right, bottom = self.crop_box
            cropped_img = self.current_image.crop((left, top, right, bottom))
            new_img_path = os.path.join(self.image_dir, f"cropped_{self.images[self.image_index]}")
            cropped_img.save(new_img_path)
            messagebox.showinfo("Info", f"Image saved as {new_img_path}")
            self.image_index += 1
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = CropTool(root)
    root.mainloop()
    