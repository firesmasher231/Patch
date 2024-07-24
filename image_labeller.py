import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil


class ImageLabeler:
    def __init__(self, root, image_folder, output_folder):
        self.root = root
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.images = [
            f
            for f in os.listdir(image_folder)
            if f.lower().endswith(("png", "jpg", "jpeg"))
        ]
        self.index = 0
        self.setup_gui()
        self.show_image()

    def setup_gui(self):
        self.root.title("Image Labeler")

        self.image_panel = tk.Label(self.root)
        self.image_panel.pack()

        self.label_frame = tk.Frame(self.root)
        self.label_frame.pack()

        self.well_maintained_btn = tk.Button(
            self.label_frame,
            text="Well Maintained (1)",
            command=lambda: self.label_image("well_maintained"),
        )
        self.well_maintained_btn.grid(row=0, column=0)

        self.partially_maintained_btn = tk.Button(
            self.label_frame,
            text="Partially Maintained (2)",
            command=lambda: self.label_image("partially_maintained"),
        )
        self.partially_maintained_btn.grid(row=0, column=1)

        self.overgrown_btn = tk.Button(
            self.label_frame,
            text="Overgrown (3)",
            command=lambda: self.label_image("overgrown"),
        )
        self.overgrown_btn.grid(row=0, column=2)

        self.skip_btn = tk.Button(
            self.label_frame, text="Skip (0)", command=self.skip_image
        )
        self.skip_btn.grid(row=0, column=3)

        self.root.bind("1", lambda event: self.label_image("well_maintained"))
        self.root.bind("2", lambda event: self.label_image("partially_maintained"))
        self.root.bind("3", lambda event: self.label_image("overgrown"))
        self.root.bind("0", lambda event: self.skip_image())

    def show_image(self):
        if self.index < len(self.images):
            image_path = os.path.join(self.image_folder, self.images[self.index])
            image = Image.open(image_path)
            image = image.resize((800, 600), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            self.image_panel.configure(image=image)
            self.image_panel.image = image
        else:
            self.root.quit()

    def label_image(self, label):
        if self.index < len(self.images):
            image_name = self.images[self.index]
            label_folder = os.path.join(self.output_folder, label)
            if not os.path.exists(label_folder):
                os.makedirs(label_folder)
            shutil.move(
                os.path.join(self.image_folder, image_name),
                os.path.join(label_folder, image_name),
            )
            self.index += 1
            self.show_image()

    def skip_image(self):
        if self.index < len(self.images):
            self.index += 1
            self.show_image()


def main():
    root = tk.Tk()
    # image_folder = filedialog.askdirectory(title="Select Image Folder")
    # output_folder = filedialog.askdirectory(title="Select Output Folder")

    # load the image folders which is the input and output folders in same directory
    image_folder = "images"
    output_folder = "output"

    if image_folder and output_folder:
        app = ImageLabeler(root, image_folder, output_folder)
        root.mainloop()


if __name__ == "__main__":
    main()
