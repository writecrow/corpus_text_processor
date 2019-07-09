#!/usr/bin/env python3

# To build for MacOS:
# pyinstaller --onefile --windowed --osx-bundle-identifier=CROW -n "Corpus Text Processor" --icon=default_icon.icns crow_processor.py
# cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
# codesign -s "CROW" dist/Corpus\ Text\ Processor.app/
# mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/
# pkgbuild --root Mac --identifier CROW --version 0.12 --install-location /Applications CorpusTextProcessor.pkg --sign "John Fullmer"

# To build for Windows:
# pyinstaller --onfile -wF crow_processor.py
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI
import convert_to_utf8
import normalization
import os
print = sg.EasyPrint

sg.ChangeLookAndFeel('TealMono')
layout = [
    [sg.Text('Corpus Text Processor', size=(30, 1), font=("Verdana", 20))],
    [sg.Text('IMPORTANT PREPARATORY STEP:')],
    [sg.Text('Copy files to be processed into a new folder on your computer (processors will overwrite these files)')],
    [sg.Text('Choose folder:', size=(20, 1)),
        sg.InputText(""), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Choose processors:', size=(20, 1))],
    [sg.Radio('Standardize to UTF-8 encoding (overwrites files)', "Processors", default=True)],
    [sg.Radio('Normalize characters (saved to "normalized" folder)', "Processors", default=True)],
    [sg.Button("Process files", size=(12, 1)), sg.Exit(size=(6, 1))]
]
window = sg.Window('Corpus Text Processor', keep_on_top=False, font=(
    "Verdana", 14), default_element_size=(40, 1)).Layout(layout)


def process_recursive(values):
    # values[0] is the directory to be processed
    directory = values[0]
    # values[1] is UTF-8 Conversion
    # values[2] is Normalization
    if values[1] is True:
        print("*** CONVERTING TO UTF-8 ***")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                convert_to_utf8.convert(os.path.join(dirpath, name), name)
    if values[2] is True:
        print("")
        print("*** NORMALIZING CHARACTERS ***")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                this_file = os.path.join(dirpath, name)
                if (os.path.splitext(name)[1]) == ".txt":
                    normalization.normalize(os.path.join(dirpath, name), directory, name)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == "Process files" and values[0] is not None and os.path.isdir(values[0]):
        process_recursive(values)
    else:
        print("You need to provide a valid folder")

window.Close()
