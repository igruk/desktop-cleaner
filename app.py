import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date

from config import CONFIG, FILE_TYPES


class DesktopCleanerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Cleaner")
        self.root.geometry("450x250+500+300")

        self.language = "en"
        self.enabled = tk.IntVar()

        self.language_button = ttk.Button(text=CONFIG[self.language]['language_button_text'],
                                          command=self.change_language)
        self.language_button.pack(padx=5, pady=5, anchor="ne")

        self.label = ttk.Label(text=CONFIG[self.language]['label_text'],
                               font=("Courier New", 14))
        self.label.pack(pady=8)

        self.open_button = ttk.Button(text=CONFIG[self.language]['open_button_text'],
                                      command=self.open_directory)
        self.open_button.pack(pady=8, ipady=3, expand=True)

        self.path_label = ttk.Label(text='')
        self.path_label.pack(anchor="n", expand=True)

        self.check_label = ttk.Label(text='')
        self.check_label.pack(anchor="n", expand=True)

        self.start_button = ttk.Button(text=CONFIG[self.language]['start_button_text'],
                                       command=self.move_files,
                                       state=tk.DISABLED)
        self.start_button.pack(expand=True, ipady=10)

        self.check_button = ttk.Checkbutton(text=CONFIG[self.language]['check_button_text'],
                                            variable=self.enabled)
        self.check_button.pack(expand=True, padx=5, pady=5, anchor="sw")

        self.update_language()

    def change_language(self):
        """Change the interface language"""
        self.language = 'ua' if self.language == 'en' else 'en'
        self.update_language()

    def update_language(self):
        """Update the language translations for the UI"""
        translations = CONFIG[self.language]
        self.language_button["text"] = translations['language_button_text']
        self.open_button["text"] = translations['open_button_text']
        self.start_button["text"] = translations['start_button_text']
        self.check_button["text"] = translations['check_button_text']
        self.label["text"] = translations['label_text']
        self.root.title("Desktop Cleaner")

    def open_directory(self):
        """Choose the path to the folder"""
        self.path = filedialog.askdirectory()

        if self.path:
            self.check_label["text"] = ''
            self.path_label["text"] = f'{self.path[:3]}.../{os.path.split(self.path)[-1]}'
            self.start_button["state"] = tk.NORMAL
        else:
            self.check_label["text"] = ''
            self.path_label["text"] = ''
            self.start_button["state"] = tk.DISABLED

    def move_file(self, source, destination, filename):
        """Move the file to a new folder if it is not there"""
        try:
            shutil.move(source, destination)
        except shutil.Error:
            message = CONFIG[self.language]['file_exists_message'].format(file=filename)
            messagebox.showinfo(title=CONFIG[self.language]['info_title'], message=message)

    def move_files(self):
        """Move files from the desktop to a new folder"""
        file_list = os.listdir(self.path)
        dir_name = 'desktop-' + str(date.today())
        dir_path = os.path.join(self.path, dir_name)
        os.makedirs(dir_path, exist_ok=True)

        for filename in file_list:
            source = os.path.join(self.path, filename)
            file_type = os.path.splitext(filename)[1][1:].lower()
            type_dir_path = os.path.join(dir_path, file_type) if file_type else os.path.join(dir_path, 'folders')

            if not self.enabled.get():
                if file_type and file_type not in FILE_TYPES:
                    type_dir_path = os.path.join(dir_path, file_type)
                    os.makedirs(type_dir_path, exist_ok=True)
                    self.move_file(source, type_dir_path, filename)

            else:
                os.makedirs(type_dir_path, exist_ok=True)
                if dir_path != source:
                    self.move_file(source, type_dir_path, filename)

        self.check_label["text"] = "✓"
        self.check_label["font"] = ("Courier New", 14)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopCleanerApp()
    app.run()
