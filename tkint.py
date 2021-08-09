#!/usr/bin/env python3
# pylint: disable=E1101

# Base imports
import os
import base64
from tabulate import tabulate

# The following are the available custom processors.
from processors import convert_to_plaintext
from processors import encode_to_utf8
from processors import standardize_characters
from processors import remove_pdf_metadata

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter.ttk import Progressbar

gui = Tk()
gui.geometry("700x300")
gui.title("Corpus Text Processor")

source = StringVar()
destination = StringVar()
processor = StringVar()
# action.set("convertToPlaintext")

def getSourcePath():
    folder_selected = filedialog.askdirectory()
    source.set(folder_selected)

def getDestinationPath():
    folder_selected = filedialog.askdirectory()
    destination.set(folder_selected)

def doStuff():
    dest = destination.get()
    # action = action.get()
    p = processor.get()
    print(p)
    print(dest)
    # showinfo(
    #     title='Result',
    #     message=source.get()
    # )
    import time
    progress['value'] = 20
    gui.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    gui.update_idletasks()
    time.sleep(1)

    progress['value'] = 50
    gui.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    gui.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    gui.update_idletasks()
    time.sleep(1)
    progress['value'] = 100

a = Label(gui ,text="Select folder to process:")
a.grid(row=0,column = 0)
E = Entry(gui,textvariable=source)
E.grid(row=0,column=1)
btnFind = ttk.Button(gui, text="Browse",command=getSourcePath)
btnFind.grid(row=0,column=2)

b = Label(gui ,text="Save files to:")
b.grid(row=1,column = 0)
F = Entry(gui,textvariable=destination)
F.grid(row=1,column=1)
btnFind = ttk.Button(gui, text="Browse",command=getDestinationPath)
btnFind.grid(row=1,column=2)

# action = "convertToPlaintext"
btn1 = Radiobutton(gui, text="Convert to plaintext (supports .docx, .html, .pdf, .pptx, .rtf)", variable=processor, value="convertToPlaintext").grid(row=4, column=1)
btn2 = Radiobutton(gui, text="Encode in UTF-8 (expects .txt files)", variable=processor, value="encodeUtf8").grid(row=5, column=1)

c = ttk.Button(gui ,text="Process files", command=doStuff)
c.grid(row=7,column=0)

progress = Progressbar(gui, orient = HORIZONTAL, length = 100, mode = 'determinate')

progress.grid(column=9, row=1, columnspan=1, padx=10, pady=20)


gui.mainloop()
