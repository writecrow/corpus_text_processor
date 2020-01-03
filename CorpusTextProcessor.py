#!/usr/bin/env python3
# pylint: disable=E1101

# Base imports
import os
from tabulate import tabulate

import PySimpleGUIQt as sg
# Windows can use PySimpleGUI

# The following are the available custom processors.
from processors import convert_to_plaintext
from processors import encode_to_utf8
from processors import standardize_characters
from processors import remove_pdf_metadata

# Set the 'print' command to use the GUI.
print = sg.Print

# Define the GUI.
sg.ChangeLookAndFeel('TealMono')
layout = [
    [sg.Text('Process files from:', size=(20, 1)),
        sg.InputText("", key='source'), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Save files to:', size=(20, 1)),
        sg.InputText("", key='destination'), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Choose processor:', size=(20, 1))],
    [sg.Radio("Convert to plaintext (supports .docx, .pdf, .html, .pptx)",
              "Processors", key='convertToPlaintext', default=True)],
    [sg.Radio("Encode in UTF-8 (expects .txt files)",
              "Processors", key='encodeUtf8', default=False)],
    [sg.Radio("Standardize non-ASCII characters and remove non-English characters (expects UTF-8 encoded input)",
              "Processors", key='standardizeCharacters', default=False)],
    [sg.Radio("Remove PDF metadata (i.e., authoring information). Expects .pdf files.",
              "Processors", key='removeMetadata', default=False)],
    [sg.Button("Process files", size=(20, 1)), sg.Exit(size=(6, 1))],
    [sg.ProgressBar(max_value=10, orientation='h', size=(80, 20), key='progress')],
    [sg.Text('', size=(80, 1), key='result_text')],
    [sg.Text('', size=(80, 1), key='progress_text')],
]
window = sg.Window('Corpus Text Processor', keep_on_top=False, font=("Helvetica", 14), default_element_size=(50, 1)).Layout(layout)
progress_bar = window['progress']
progress_text = window['progress_text']
result_text = window['result_text']


def process_recursive(values):
    source = values['source']
    destination = values['destination']
    resultList = []
    supported_filetypes = ['.docx', '.pdf', '.html', '.pptx', '.txt', '.doc']

    # Reset the progress in the GUI.
    inc = 0
    total_files = 0
    progress_bar.update_bar(inc)

    # Calculate the number of files to be processed.
    for dirpath, dirnames, files in os.walk(values['source']):
        for filename in files:
            file_parts = os.path.splitext(filename)
            extension = file_parts[1].lower()
            # Only count supported filetypes.
            if extension in supported_filetypes:
                total_files = total_files + 1

    # Loop through all files found in the source directory.
    for dirpath, dirnames, files in os.walk(values['source']):
        for filename in files:
            # Extract the file extension.
            file_parts = os.path.splitext(filename)
            extension = file_parts[1].lower()

            # Skip unsupported files.
            if extension not in supported_filetypes:
                continue

            # Get the absolute path to the current file
            filepath = os.path.join(dirpath, filename)

            # Perform the user-selected operation.
            if values['convertToPlaintext'] is True:
                processor = convert_to_plaintext
            elif values['encodeUtf8'] is True:
                processor = encode_to_utf8
            elif values['standardizeCharacters'] is True:
                processor = standardize_characters
            elif values['removeMetadata'] is True:
                processor = remove_pdf_metadata
            result = processor.run(filepath, source, destination, filename, extension)
            resultList.append(result)

            # Update the progress in the GUI.
            inc = inc + 1
            progress_bar.update_bar(inc/total_files*10)
            progress_text.Update('Processing ' + filename + ' : ' + result['message'])
            result_text.Update(str(inc) + ' of ' + str(total_files))

    # Process results for output.
    failed = []
    succeeded = []
    for i in resultList:
        if i['result'] is True:
            succeeded.append([i['name'], i['message']])
        else:
            failed.append([i['name'], i['message']])

    print(' ')
    print('**********************************************************')
    print('******** The following were successfully processed *******')
    print(tabulate(succeeded, headers=['Filename', 'Message']))
    print(' ')
    print('**********************************************************')
    print(' ')
    # Print failures, if present.
    if (len(failed) > 0):
        print('***** WARNING: The following failed or were skipped: *****')
        print(tabulate(failed, headers=['Filename', 'Message']))
        print(' ')
    else:
        print('*********** ALL FILES SUCCESSFULLY PROCESSED! ************')
    print('**********************************************************')
    print('Success count: ', len(succeeded))
    print('Failure/skipped count: ', len(failed))
    print('**********************************************************')


while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == "Process files" and values['source'] is not None and os.path.isdir(values['source']) and values['destination'] is not None and os.path.isdir(values['destination']):
        process_recursive(values)
    else:
        print("Provide valid 'from' and 'to' folders.")

window.Close()
