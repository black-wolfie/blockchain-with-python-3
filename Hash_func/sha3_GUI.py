# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:16:39 2018
"""
from tkinter import Tk, Label, Button
import hashlib
from tkinter.filedialog import askopenfilenames
import os
import pandas as pd

# file dialog function
def OpenFile():
    files = askopenfilenames(initialdir="C:/",
                             filetypes =(("All Files","*.*"),
                                        (".exe Files","*.exe"),
                                        (".txt File", "*.txt")),
                             title = "Choose files to apply SHA2-256 hashing")
    sha3_256_tb = sha3_gui_func(files)
    return sha3_256_tb

# sha2 hashing algorithm, outputs hash functions
def sha3_gui_func(files):
    BLOCKSIZE = 65536*100
    h_sha3_256 = hashlib.sha3_256()
    n = len(files)
    
    lb2 = Label(window_1, text = "File Name", font=("Consolas", 10))
    lb2.grid(row=4, column=1) 
    lb2 = Label(window_1, text = "sha3-256 hash", font=("Consolas", 10))
    lb2.grid(row=4, column=2) 
    sha3_256_tb = pd.DataFrame([])
    
    for x in range(0,n):
        h_sha3_256 = hashlib.sha3_256()
        with open(files[x], 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                h_sha3_256.update(buf)
                buf = afile.read(BLOCKSIZE)
   
        sha3_256_dict = {"File_Name":[os.path.basename(files[x])],
                         "SHA3_256_hash":[h_sha3_256.hexdigest()]}
        
        sha3_256_tb = sha3_256_tb.append(pd.DataFrame(sha3_256_dict))
    
        # isolate file name from path: os.path.basename(your_path)
        # abbreviate file names that are too long
        if len(os.path.basename(files[x])) > 25:
            lb_x = Label(window_1, text = ("..." +
                    os.path.basename(files[x])[-25:] + " :"), 
                    font = ("Consolas", 10))
        else:
            lb_x = Label(window_1, text = (os.path.basename(files[x])+ " :"), 
                    font = ("Consolas", 10))
        
        lb_x.grid(sticky="W", row = x + 5, column = 1)
        
        lb_hash = Label(window_1, text = h_sha3_256.hexdigest(), 
                        font = ("Consolas", 10))
        lb_hash.grid(sticky="E", row = x + 5, column = 2)
    return sha3_256_tb

# setup the main window_1
window_1 = Tk()
window_1.geometry('700x600+650+200')
window_1.title("SHA3-256 hasher")

lb0 = Label(window_1, text = "+", font=("Ariel", 5))
lb0.grid(sticky="W", row=0, column=0)

lbl = Label(window_1, text = "Selet the files you want to hash", 
                font=("Ariel", 10))
lbl.grid(sticky="W", row=1, column=1)

btn = Button(window_1, text="Select Files", command =  OpenFile)
btn.grid(row = 3, column = 1)
window_1.mainloop()
