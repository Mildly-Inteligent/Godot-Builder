import tkinter as tk
from tkinter import filedialog as fd
import shutil
import os
import re


root = tk.Tk()
root.title("Godot source builder")



_source_directory = "Empty"
_custom_modules = []


def DeadSpace(size:int):
    return tk.Label(root, text= ' ', font= ("Arial", size))


def select_folder():
    directoryPath = fd.askdirectory(
        title= "Godot source code root folder:",
        initialdir= '/',
        mustexist= True
    )

    return directoryPath
def select_source():
    global _source_directory

    path = select_folder()

    if path != "":
        _source_directory = path
        sourceDirectoryName.config(text= path)
        selectFolder.config(text= "Change folder")
def add_custom_module():
    global _custom_modules

    path = select_folder()
    if path != "":
        custom_modules.insert("end", path)
        _custom_modules.append(path)
def edit_custom_module_path():
    global _custom_modules

    index = custom_modules.curselection()
    if len(index) == 1:
        index = int(index[0])
    else:   return
    path = select_folder()
    if path != "":
        custom_modules.delete(index, index)
        custom_modules.insert(index, path)
        _custom_modules.pop(index)
        _custom_modules.insert(index, path)
def remove_custom_module():
    global _custom_modules

    index = custom_modules.curselection()
    if len(index) == 1:
        index = int(index[0])
    custom_modules.delete(index, index)
    _custom_modules.pop(index)



def build():
    os.system("pip install scons")
    regex_pattern1 = r"void initialize_([\w-]+)_module\(ModuleInitializationLevel p_level\);"
    regex_pattern2 = r"void uninitialize_([\w-]+)_module\(ModuleInitializationLevel p_level\);"
    for module in _custom_modules:
        f = open(f"{module}/register_types.h", 'r').read()
        match1 = re.search(regex_pattern1, f)
        match2 = re.search(regex_pattern2, f)
        if match1 and match2:
            if match1.group(1) == match2.group(1):
                target_dir = f"{_source_directory}/modules/{match1.group(1)}"
                if os.path.exists(target_dir):  continue

                shutil.copytree(module, target_dir)



    os.chdir(_source_directory)
    os.system(f"python -m SCons p=windows")

    postBuildMSG.grid(row=14, column=0, columnspan=4)



header = tk.Label(root, text= "Godot source builder:", font= ("Arial", 32, "bold"))
sourceDirectoryH = tk.Label(root, text= "Source directory path:", font= ("Arial", 24))
sourceDirectoryHelp = tk.Label(root, text= "This is the folder containing the source code for Godot.", font= ("Arial", 14), fg= "gray40")
selectFolder = tk.Button(root, text= "Open folder", command= select_source)
sourceDirectoryPretext = tk.Label(root, text= f"Source directory: ", font= ("Arial", 16))
sourceDirectoryName = tk.Label(root, text= _source_directory, font= ("Courier New", 16), bg= "gray75")
customModulesH = tk.Label(root, text= "Custom modules:", font= ("Arial", 24))
customModulesHelp = tk.Label(root, text= "Add any custom modules to the compiled program.", font= ("Arial", 14), fg= "gray40")
custom_modules = tk.Listbox(root, font= ("Courier New", 12), width= 30, height= 10)
scrollbar = tk.Scrollbar(root, orient= "vertical")
customModulesNotice = tk.Label(root, text= "*Please note some folder names will be changed in the source.", font= ("Arial", 14), fg= "gray40")
ADDbutton = tk.Button(root, text= "Add module", font= ("Arial", 12), command= add_custom_module)
EDITbutton = tk.Button(root, text= "Edit path", font= ("Arial", 12), command= edit_custom_module_path)
REMOVEbutton = tk.Button(root, text= "Remove module", font= ("Arial", 12), command= remove_custom_module)
warning = tk.Label(root, text= "The building procces will take 10-15 minuets.\nFeel free to use your device as normal whilst building.", font= ("Arial", 16))
buildButton = tk.Button(root, text= "Build", font= ("Arial", 32, "bold"), command= build)
postBuildMSG = tk.Label(root, text= f"The compiled exe is located in {_source_directory}/bin/", font= ("Arial", 32))


scrollbar.configure(command=custom_modules.yview)
custom_modules.configure(yscrollcommand=scrollbar.set)

header.grid(row=0, column=0, columnspan=4)
DeadSpace(32).grid(row=1, column=0, columnspan=4)

sourceDirectoryH.grid(row=2, column=0, columnspan=4)
sourceDirectoryHelp.grid(row=3, column=0, columnspan=4)
selectFolder.grid(row=4, column=0, columnspan=2)
sourceDirectoryPretext.grid(row=4, column=2, sticky= 'w')
sourceDirectoryName.grid(row=4, column=3, columnspan=2, sticky= 'w')
DeadSpace(32).grid(row=5, column=0, columnspan=4)

customModulesH.grid(row=6, column=0, columnspan=4)
customModulesHelp.grid(row=7, column=0, columnspan=4)
ADDbutton.grid(row=8, column=0)
EDITbutton.grid(row=8, column=1)
REMOVEbutton.grid(row=8, column=2)
custom_modules.grid(row=9, column=0, columnspan=3, sticky='ew')
scrollbar.grid(row=9, column=3, sticky='nsw')
customModulesNotice.grid(row=10, column=0, columnspan=4)
DeadSpace(32).grid(row=11, column=0, columnspan=4)

warning.grid(row=12, column=0, columnspan=4)
buildButton.grid(row=13, column=0, columnspan=4)


root.mainloop()
