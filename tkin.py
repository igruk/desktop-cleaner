from tkinter import ttk, IntVar, Tk, filedialog
from tkinter.messagebox import showinfo
from datetime import date
import shutil
import os


def open_directory():
    """Choose the path to the folder"""
    global path
    path = filedialog.askdirectory()

    if path != '':
        check_label["text"] = ''
        path_label["text"] = path[:3] + '.../' + path.split('/')[-1]
        start_button["state"] = "enabled"

    else:
        check_label["text"] = ''
        path_label["text"] = ''
        start_button["state"] = "disabled"


def change_language():
    """Change the interface language"""
    global language

    if language == "en":
        language = "ua"
        open_button["text"] = "Вибрати папку"
        start_button["text"] = "Старт"
        checkbutton["text"] = "Включно з ярликами і папками"
        label["text"] = "Очисти Робочий стіл в один клік!"
    else:
        language = "en"
        open_button["text"] = "Select Folder"
        start_button["text"] = "Start"
        checkbutton["text"] = "Include Shortcuts and Folders"
        label["text"] = "Clear Desktop in one Click!"


def start():
    """Start app"""
    file_list = os.listdir(path)  # list of files in the selected folder (on the desktop)

    dir_name = 'desktop-' + str(date.today())  # the folder where the files will be moved
    dir_path = path + '/' + dir_name  # path to the folder

    if not os.path.exists(dir_path):  # if the folder does not exist - create it
        os.mkdir(dir_path)

    for file in file_list:
        source = path + '/' + file  # path to the file in the selected folder

        if enabled.get() == 0:  # if you don't need to include shortcuts and folders
            if os.path.isfile(source):
                file_type = source.split('.')[-1]  # if it is a file - defines the type

                if file_type != 'lnk' and file_type != 'url':  # not include shortcuts
                    type_dir_path = dir_path + '/' + file_type  # path to the folder of a specific type

                    if not os.path.exists(type_dir_path):
                        os.mkdir(type_dir_path)

                    try:
                        shutil.move(source, type_dir_path)  # move the file
                    except shutil.Error:
                        if language == 'en':
                            showinfo(title='Info',
                                     message=f'File with name "{file}" already exists and won\'t be moved')
                        else:
                            showinfo(title='Повтор',
                                     message=f'Файл "{file}" вже існує і не буде переміщений')

        else:  # if you need to include shortcuts and folders
            if os.path.isfile(source):
                file_type = source.split('.')[-1]  # if it is a file - defines the type
                type_dir_path = dir_path + '/' + file_type

                if not os.path.exists(type_dir_path):
                    os.mkdir(type_dir_path)

                try:
                    shutil.move(source, type_dir_path)
                except shutil.Error:
                    if language == 'en':
                        showinfo(title='Info', 
                                 message=f'File with name "{file}" already exists and won\'t be moved')
                    else:
                        showinfo(title='Повтор', message=f'Файл "{file}" вже існує і не буде переміщений')

            else:  # if directory
                folder_dir_path = dir_path + '/folders'  # path to folder with sub-folders

                if not os.path.exists(folder_dir_path):
                    os.mkdir(folder_dir_path)

                if dir_path != source:
                    try:
                        shutil.move(source, folder_dir_path)
                    except shutil.Error:
                        if language == 'en':
                            showinfo(title='Info',
                                     message=f'Folder with name "{file}" already exists and won\'t be moved')
                        else:
                            showinfo(title='Повтор', message=f'Папка "{file}" вже існує і не буде переміщена')

    check_label["text"] = "✓"
    check_label["font"] = ("Courier New", 14)


root = Tk()
root.title("Desktop Cleaner")
root.geometry("450x250+500+300")

language = "en"

language_button = ttk.Button(text="UA / EN", command=change_language)
language_button.pack(padx=5, pady=5, anchor="ne")

label = ttk.Label(text="Clear Desktop in one Click!", font=("Courier New", 14))
label.pack(pady=8)

open_button = ttk.Button(text="Select Folder", command=open_directory)
open_button.pack(pady=8, ipady=3, expand=True)

path_label = ttk.Label(text='')
path_label.pack(anchor="n", expand=True)

check_label = ttk.Label(text='')
check_label.pack(anchor="n", expand=True)

start_button = ttk.Button(text="Start", command=start, state="disabled")
start_button.pack(expand=True, ipady=10)

enabled = IntVar()

checkbutton = ttk.Checkbutton(text="Include Shortcuts and Folders", variable=enabled)
checkbutton.pack(expand=True, padx=5, pady=5, anchor="sw")

root.mainloop()
