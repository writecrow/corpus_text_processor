#!/usr/bin/env python3

# To build for MacOS:
# pyinstaller --onefile --windowed --osx-bundle-identifier=CROW -n "Corpus Text Processor" --icon=default_icon.icns CorpusTextProcessor.py
#
# cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
# codesign -s "CROW" dist/Corpus\ Text\ Processor.app/
#
# mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/
# pkgbuild --root Mac --identifier CROW --version 0.alpha4 --install-location /Applications CorpusTextProcessor-unsigned.pkg --sign "John Fullmer"

# https://simplemdm.com/certificate-sign-macos-packages/
# productsign --sign "3rd Party Mac Developer Installer: John Fullmer (A57QZ4FF3C)" CorpusTextProcessor-unsigned.pkg CorpusTextProcessor.pkg

# To build for Windows:
# pyinstaller --onefile -wF CorpusTextProcessor.py --icon=default_icon.ico --manifest AppxManifest.xml
#
# https://docs.microsoft.com/en-us/windows/uwp/packaging/create-certificate-package-signing
# New-SelfSignedCertificate -Type Custom -Subject "CN=WriteCrow, O=WriteCrow, C=US" -KeyUsage DigitalSignature -FriendlyName "Crow, the corpus & repository of writing" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")
# $pwd = ConvertTo-SecureString -String <PASSWORD> -Force -AsPlainText
# Export-PfxCertificate -cert "Cert:\CurrentUser\My\E47982D297DB2BD3A412B3FD3C96094A02F9202F" -FilePath C:\Users\mark\writecrow-cert.pfx -Password $pwd
# SignTool sign /fd SHA256 /a /f C:\Users\mark\writecrow-cert.pfx /p <PASSWORD> dist\gui.exe

import PySimpleGUI as sg
# Windows can use PySimpleGUI
import convert_to_plaintext
import convert_to_utf8
import normalization
import os
print = sg.EasyPrint

sg.ChangeLookAndFeel('TealMono')
layout = [
    [sg.Text('Corpus Text Processor', size=(30, 1), font=("Verdana", 20))],
    [sg.Text('Process files from:', size=(20, 1)),
        sg.InputText(""), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Save files to:', size=(20, 1)),
        sg.InputText(""), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Choose processor:', size=(20, 1))],
    [sg.Radio("Convert to plaintext",
              "Processors", default=False)],
    [sg.Radio("Standardize to UTF-8 encoding",
              "Processors", default=False)],
    [sg.Radio("Normalize characters",
              "Processors", default=False)],
    [sg.Button("Process files", size=(12, 1)), sg.Exit(size=(6, 1))]
]
window = sg.Window('Corpus Text Processor', keep_on_top=False, font=(
    "Verdana", 14), default_element_size=(40, 1)).Layout(layout)


def process_recursive(values):
    # values[0] is the directory to be processed
    from_directory = values[0]
    to_directory = values[1]
    # values[2] is Plaintext
    # values[3] is UTF-8 Conversion
    # values[4] is Normalization
    if values[2] is True:
        supported_filetypes = ['.docx', '.pdf', '.html', '.pptx', '.txt']
        print("*** CONVERTING TO PLAINTEXT ***")
        for dirpath, dirnames, files in os.walk(from_directory):
            for name in files:
                extension = os.path.splitext(name)[1]
                if extension in supported_filetypes:
                    convert_to_plaintext.convert(os.path.join(
                        dirpath, name), from_directory, to_directory, name, extension)
        print("*** COMPLETED ***")
    if values[3] is True:
        print("*** CONVERTING TO UTF-8 ***")
        for dirpath, dirnames, files in os.walk(from_directory):
            for name in files:
                extension = os.path.splitext(name)[1]
                if extension == ".txt":
                    convert_to_utf8.convert(os.path.join(dirpath, name), from_directory, to_directory, name)
        print("*** COMPLETED ***")
    if values[4] is True:
        print("*** NORMALIZING CHARACTERS ***")
        for dirpath, dirnames, files in os.walk(from_directory):
            for name in files:
                extension = os.path.splitext(name)[1]
                if extension == ".txt":
                    normalization.normalize(os.path.join(dirpath, name), from_directory, to_directory, name)
        print("*** COMPLETED ***")

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == "Process files" and values[0] is not None and os.path.isdir(values[0]) and values[1] is not None and os.path.isdir(values[1]):
        process_recursive(values)
    else:
        print("You need to provide a valid folder")

window.Close()
