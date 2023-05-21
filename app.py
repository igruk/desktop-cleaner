import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date

from config import CONFIG, FILE_TYPES


def open_directory():
    """Choose the path to the folder"""
    global path
    path = filedialog.askdirectory()

    if path:
        check_label["text"] = ''
        path_label["text"] = f'{path[:3]}.../{os.path.split(path)[-1]}'
        start_button["state"] = tk.NORMAL
    else:
        check_label["text"] = ''
        path_label["text"] = ''
        start_button["state"] = tk.DISABLED


def change_language():
    """Change the interface language"""
    global language
    language = 'ua' if language == 'en' else 'en'
    update_language()


def update_language():
    """Update the language translations for the UI"""
    translations = CONFIG[language]
    language_button["text"] = translations['language_button_text']
    open_button["text"] = translations['open_button_text']
    start_button["text"] = translations['start_button_text']
    check_button["text"] = translations['check_button_text']
    label["text"] = translations['label_text']
    root.title("Desktop Cleaner")


def move_files():
    """Move files from the desktop to a new folder"""
    file_list = os.listdir(path)  # list of files in the selected folder (on the desktop)

    dir_name = 'desktop-' + str(date.today())  # the folder where the files will be moved
    dir_path = os.path.join(path, dir_name)  # path to the folder

    if not os.path.exists(dir_path):  # if the folder does not exist, create it
        os.mkdir(dir_path)

    for file in file_list:
        source = os.path.join(path, file)  # path to the file in the selected folder

        if enabled.get() == 0:  # if you don't need to include shortcuts and folders
            if os.path.isfile(source):
                file_type = source.split('.')[-1]  # if it is a file, determine the type

                if file_type not in FILE_TYPES:  # do not include shortcuts
                    type_dir_path = os.path.join(dir_path, file_type)  # path to the folder of a specific type

                    if not os.path.exists(type_dir_path):
                        os.mkdir(type_dir_path)

                    try:
                        shutil.move(source, type_dir_path)  # move the file
                    except shutil.Error:
                        message = CONFIG[language]['file_exists_message'].format(file=file)
                        messagebox.showinfo(title=CONFIG[language]['info_title'], message=message)

        else:  # if you need to include shortcuts and folders
            if os.path.isfile(source):
                file_type = source.split('.')[-1]  # if it is a file, determine the type
                type_dir_path = os.path.join(dir_path, file_type)

                if not os.path.exists(type_dir_path):
                    os.mkdir(type_dir_path)

                try:
                    shutil.move(source, type_dir_path)
                except shutil.Error:
                    message = CONFIG[language]['file_exists_message'].format(file=file)
                    messagebox.showinfo(title=CONFIG[language]['info_title'], message=message)

            else:  # if directory
                folder_dir_path = os.path.join(dir_path, 'folders')  # path to folder with sub-folders

                if not os.path.exists(folder_dir_path):
                    os.mkdir(folder_dir_path)

                if dir_path != source:
                    try:
                        shutil.move(source, folder_dir_path)
                    except shutil.Error:
                        message = CONFIG[language]['folder_exists_message'].format(folder=file)
                        messagebox.showinfo(title=CONFIG[language]['info_title'], message=message)

    check_label["text"] = "✓"
    check_label["font"] = ("Courier New", 14)


root = tk.Tk()
root.title("Desktop Cleaner")
root.geometry("450x250+500+300")

language = "en"
enabled = tk.IntVar()

language_button = ttk.Button(text=CONFIG[language]['language_button_text'], command=change_language)
language_button.pack(padx=5, pady=5, anchor="ne")

label = ttk.Label(text=CONFIG[language]['label_text'], font=("Courier New", 14))
label.pack(pady=8)

open_button = ttk.Button(text=CONFIG[language]['open_button_text'], command=open_directory)
open_button.pack(pady=8, ipady=3, expand=True)

path_label = ttk.Label(text='')
path_label.pack(anchor="n", expand=True)

check_label = ttk.Label(text='')
check_label.pack(anchor="n", expand=True)

start_button = ttk.Button(text=CONFIG[language]['start_button_text'], command=move_files, state=tk.DISABLED)
start_button.pack(expand=True, ipady=10)

check_button = ttk.Checkbutton(text=CONFIG[language]['check_button_text'], variable=enabled)
check_button.pack(expand=True, padx=5, pady=5, anchor="sw")

update_language()  # Update the language translations initially

root.mainloop()
