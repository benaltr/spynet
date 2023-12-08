import os
import cv2
import tkinter as tk
import customtkinter as ctk

from PIL import Image
from customtkinter.windows.widgets.image.ctk_image import ImageTk
from config import config

config.read("config.ini")


class GalleryApp:
    def __init__(self, folder_path, master):
        # set color
        view = config["Gallery"]
        ctk.set_appearance_mode(view["mode"])
        ctk.set_default_color_theme(view["theme"])

        self.folder_path = folder_path
        self.files = self.load_files()
        self.current_index = 0

        self.root = ctk.CTkToplevel(master)
        self.root.title("Gallery App")

        self.image_label = ctk.CTkLabel(self.root)
        self.image_label.pack()

        self.prev_button = ctk.CTkButton(self.root, text="Previous", command=self.show_previous)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = ctk.CTkButton(self.root, text="Next", command=self.show_next)
        self.next_button.pack(side=tk.RIGHT)

        self.show_media()

    def load_files(self):
        files = []
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path):
                files.append(file_path)
        return files

    def show_media(self):
        current_file = self.files[self.current_index]
        if current_file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            self.show_image(current_file)
        elif current_file.lower().endswith((".mp4", ".avi", ".mov")):
            self.play_video(current_file)

    def show_image(self, file_path):
        image = Image.open(file_path)
        image = self.resize_image(image)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def play_video(self, file_path):
        video_capture = cv2.VideoCapture(file_path)

        def show_frame():
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = self.resize_image(image)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
                self.image_label.after(30, show_frame)
            else:
                video_capture.release()
                self.show_next()

        show_frame()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.files)
        self.show_media()

    def show_previous(self):
        self.current_index = (self.current_index - 1) % len(self.files)
        self.show_media()

    def resize_image(self, image, max_width=800, max_height=600):
        width, height = image.size
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return image

    def run(self):
        self.root.mainloop()