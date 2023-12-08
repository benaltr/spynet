from gui import Login
from config import config
import customtkinter as ctk

if __name__ == '__main__':

    config.read("config.ini")
    view = config["Login"] # View settings of Login page

    ctk.set_appearance_mode(view["mode"]) # Mode view
    ctk.set_default_color_theme(view["theme"]) # Theme view 

    # Load Login Page
    root = ctk.CTk()
    Login(root)
    root.mainloop()
    

