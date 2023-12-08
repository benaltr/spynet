##########
# Import #
##########

from tkcalendar import Calendar
from gallery import GalleryApp
from rule import Rule
from server import run_flask_app
from multiprocessing import Process
from config import config
from db import coll_rules

import customtkinter as ctk
import tkinter as tk
import os

# Read config file
config.read("config.ini")

# Login Page
class Login:

    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("600x400")

        # Create username label and entry
        self.username_label = ctk.CTkLabel(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ctk.CTkEntry(self.master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create password label and entry
        self.password_label = ctk.CTkLabel(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create login button
        self.login_button = ctk.CTkButton(self.master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check username and password
        if username == "admin" and password == "admin":
            self.master.destroy()
            Admin()

        else:
            self.error_label = ctk.CTkLabel(self.master, text="Invalid username or password!") # Raise error message
            self.error_label.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


# Admin Page
class Admin:

    def __init__(self):

        # set color
        self.view = config["Admin"]
        ctk.set_appearance_mode(self.view["mode"])
        ctk.set_default_color_theme(self.view["theme"])

        # window settings
        self.admin_window = ctk.CTk()
        self.admin_window.title("Admin Window")
        self.admin_window.geometry("600x400")

        # Create welcome label
        self.welcome_label = ctk.CTkLabel(self.admin_window, text="Welcome, Admin!")
        self.welcome_label.pack(padx=10, pady=10)

        # Create logout button
        self.logout_button = ctk.CTkButton(self.admin_window, text="Logout", command=self.logout)
        self.logout_button.pack(anchor=ctk.NE)

        # Create "create rules" button
        self.create_rules_button = ctk.CTkButton(self.admin_window, text="Create Rules", command=self.create_rules)
        self.create_rules_button.place(x=0, y=0)

        # Create edit rules button
        self.edit_rules_button = ctk.CTkButton(self.admin_window, text="Edit Rules", command=self.edit_rules)
        self.edit_rules_button.place(x=0, y=30)

        # Create select folder button
        self.select_folder_button = ctk.CTkButton(self.admin_window, text="Select Folder", command=self.select_folder)
        self.select_folder_button.place(x=1300, y=600)

        # Create calender
        self.cal = Calendar(self.admin_window, selectmode='day', date_pattern='yyyy-mm-dd', font="Arial 32")
        self.cal.place(x=600, y=200)

        # Create select button
        self.select_button = ctk.CTkButton(self.admin_window, text="Select", command=self.select)
        self.select_button.place(x=700, y=600)

        # Create switch server
        self.switch_var = ctk.StringVar(value="disable")
        self.switch = ctk.CTkSwitch(self.admin_window, onvalue="enable", offvalue="disable",
                                    text="disable/enable server",
                                    variable=self.switch_var,
                                    command=self.run_spy)
        self.switch.place(x=0, y=60)

        self.admin_window.mainloop()

    ####################
    # Button functions #
    ####################

    def create_rules(self):
        self.admin_window.destroy()
        CreateRules()

    def edit_rules(self):
        self.admin_window.destroy()
        EditRules()

    def select(self):
        date = str(self.cal.get_date())

        # get the current directory
        current_dir = os.getcwd()

        # iterate through all the folders in the current directory
        for folder in os.listdir(current_dir):
            if folder == date:
                #os.chdir(date)
                folders = os.listdir(date)

                self.folders_cb = ctk.CTkComboBox(self.admin_window, values=folders)
                self.folders_cb.place(x=1000, y=600)

    def select_folder(self):
        folder = self.folders_cb.get()
        current_dir = os.getcwd()
        curr_date = str(self.cal.get_date())

        folder_path = fr'{current_dir}/{curr_date}/{folder}'
        self.gallery_app = GalleryApp(folder_path, self.admin_window)
        self.gallery_app.run()

    def run_spy(self):
        state = self.switch_var.get()

        if state == "enable":
            p = Process(target=run_flask_app)
            p.start()

        else:
            p = Process(target=run_flask_app)
            p.terminate()

    def logout(self):
        self.admin_window.destroy()
        ctk.set_appearance_mode(self.view["mode"])
        ctk.set_default_color_theme(self.view["theme"])
        root = ctk.CTk()
        Login(root)
        root.mainloop()

        


# Edit Rules Page
class EditRules:

    def __init__(self):

        # set color
        view = config["EditRules"]
        ctk.set_appearance_mode(view["mode"])
        ctk.set_default_color_theme(view["theme"])

        # window settings
        self.window = ctk.CTk()
        self.window.title("Edit Rules Window")
        self.window.geometry("600x400")

        # Create go back button
        self.go_back_button = ctk.CTkButton(self.window, text="Go Back", command=self.go_back)
        self.go_back_button.place(x=1300, y=30)

        # Create combobox
        options = coll_rules.distinct("rule_name")
        self.rules_cb = ctk.CTkComboBox(self.window, values=options)
        self.rules_cb.grid(row=0, column=0, padx=10, pady=10)

        # Create select button
        self.edit_rules_button = ctk.CTkButton(self.window, text="Select", command=self.select)
        self.edit_rules_button.grid(row=1, column=0, padx=10, pady=10)

        self.window.mainloop()
    
    ####################
    # Button functions #
    ####################

    def go_back(self):
        self.window.destroy()
        Admin()


    def select(self):
        self.selected_option = self.rules_cb.get()
        doc = coll_rules.find_one({"rule_name": self.selected_option})


        #action
        self.action_label = ctk.CTkLabel(self.window, text="Action: ")
        self.action_label.grid(row=2, column=0, padx=10, pady=10)
        self.action_entry = ctk.CTkEntry(self.window, placeholder_text=doc["action"])
        self.action_entry.grid(row=2, column=1, padx=10, pady=10)

        #url
        self.url_label = ctk.CTkLabel(self.window, text="URL: ")
        self.url_label.grid(row=3, column=0, padx=10, pady=10) 
        self.url_entry = ctk.CTkEntry(self.window, placeholder_text=doc["url"])
        self.url_entry.grid(row=3, column=1, padx=10, pady=10)

        #from to
        self.from_label = ctk.CTkLabel(self.window, text="From: ")
        self.from_label.grid(row=4, column=0, padx=10, pady=10)
        self.from_entry = ctk.CTkEntry(self.window, placeholder_text=doc["from"])
        self.from_entry.grid(row=4, column=1, padx=10, pady=10)

        self.to_label = ctk.CTkLabel(self.window, text="To: ")
        self.to_label.grid(row=4, column=2, padx=10, pady=10)
        self.to_entry = ctk.CTkEntry(self.window, placeholder_text=doc["to"])
        self.to_entry.grid(row=4, column=3, padx=10, pady=10)

        # Create switch(state)
        self.switch_label = ctk.CTkLabel(self.window, text="Disable/Enable: ")
        self.switch_label.grid(row=5, column=0, padx=10, pady=10)
        self.switch_var = ctk.StringVar(value=doc["state"])
        self.switch = ctk.CTkSwitch(self.window, onvalue="enable", offvalue="disable",
                                    text = ' ',
                                    variable=self.switch_var,
                                    command=self.update_state)
        self.switch.grid(row=5, column=1, padx=10, pady=10)

        # create labels
        self.created_label = ctk.CTkLabel(self.window, text="Created: ")
        self.created_label.grid(row=7, column=0, padx=10, pady=10)
        self.created_label = ctk.CTkLabel(self.window, text=doc["created"])
        self.created_label.grid(row=7, column=1, padx=10, pady=10)

        # Create submit button
        self.submit_button = ctk.CTkButton(self.window, text="Submit", command=self.update)
        self.submit_button.grid(row=8, column=1, padx=10, pady=10)

    def update_state(self):
        selected_var = self.switch_var.get()
        coll_rules.update_one({"rule_name": self.selected_option}, {"$set": {"state": selected_var}})

    def update(self):

        def check_entry(self):
            if self.get() is None or self.get() == "":
                return self._placeholder_text
        
            else: return self.get()

        coll_rules.update_one({"rule_name": self.selected_option}, {"$set": {"action": check_entry(self.action_entry)}})
        coll_rules.update_one({"rule_name": self.selected_option}, {"$set": {"url": check_entry(self.url_entry)}})
        coll_rules.update_one({"rule_name": self.selected_option}, {"$set": {"from": check_entry(self.from_entry)}})
        coll_rules.update_one({"rule_name": self.selected_option}, {"$set": {"to": check_entry(self.to_entry)}})

        self.window.destroy()
        Admin()

    

# Create Rules Page
class CreateRules:

    def __init__(self):

        # set color
        view = config["CreateRules"]
        ctk.set_appearance_mode(view["mode"])
        ctk.set_default_color_theme(view["theme"])

        # window settings
        self.window = ctk.CTk()
        self.window.title("Create Rules Window")
        self.window.geometry("600x400")

        # rule name
        self.rule_name_label = ctk.CTkLabel(self.window, text="Rule Name: ")
        self.rule_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.rule_name_entry = ctk.CTkEntry(self.window)
        self.rule_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # action
        self.actions_label = ctk.CTkLabel(self.window, text="Action: ")
        self.actions_label.grid(row=1, column=0, padx=10, pady=10)
        self.actions_cb = ctk.CTkComboBox(self.window, values=["screenshot", "record_video"])
        self.actions_cb.grid(row=1, column=1, padx=10, pady=10)

        # URL
        self.url_label = ctk.CTkLabel(self.window, text="URL: ")
        self.url_label.grid(row=2, column=0, padx=10, pady=10)
        self.url_entry = ctk.CTkEntry(self.window)
        self.url_entry.grid(row=2, column=1, padx=10, pady=10)

        # Time 
        self.from_label = ctk.CTkLabel(self.window, text="From: ")
        self.from_label.grid(row=3, column=0, padx=10, pady=10)
        self.from_entry = ctk.CTkEntry(self.window)
        self.from_entry.grid(row=3, column=1, padx=10, pady=10)

        self.to_label = ctk.CTkLabel(self.window, text="To: ")
        self.to_label.grid(row=3, column=2, padx=10, pady=10)
        self.to_entry = ctk.CTkEntry(self.window)
        self.to_entry.grid(row=3, column=3, padx=10, pady=10)

        self.switch_var = ctk.StringVar(value="disable")
        self.switch = ctk.CTkSwitch(self.window, text="disable/enable", onvalue="enable", offvalue="disable",
                                    variable=self.switch_var,
                                    command=self.update_state)
        self.switch.grid(row=4, column=1, padx=10, pady=10)
        self.state = self.switch_var.get()

        # Update button
        self.update_button = ctk.CTkButton(self.window, text="Update", command=self.update)
        self.update_button.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        # Create go back button
        self.go_back_button = ctk.CTkButton(self.window, text="Go Back", command=self.go_back)
        self.go_back_button.place(x=1300, y=30)

        self.window.mainloop()


    ####################
    # Button functions #
    ####################

    def update_state(self):
        self.state = self.switch_var.get()

    def update(self):
        rule_name = self.rule_name_entry.get()
        action = self.actions_cb.get()
        url = self.url_entry.get()
        from_ = self.from_entry.get()
        to = self.to_entry.get()

        #Check if url exist and rule name exist
        if coll_rules.find_one({"rule_name": rule_name}):
            self.error_label = ctk.CTkLabel(self.window, text="Rule name already exist!")
            self.error_label.grid(row=0, column=2, padx=10, pady=10)
            self.rule_name_entry.delete(0, tk.END)

        elif coll_rules.find_one({"url": url}):
            self.error_label = ctk.CTkLabel(self.window, text="URL already exist!")
            self.error_label.grid(row=2, column=2, padx=10, pady=10)
            self.url_entry.delete(0, tk.END)

        else:
            rule = Rule(rule_name, action, url, from_, to, self.state)
            rule.add_rule()

            self.rule_name_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)


    def go_back(self):
        self.window.destroy()
        Admin()




