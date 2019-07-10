#!/usr/local/bin/python3
# Remove PDF metadata

from PyPDF3 import PdfFileReader, PdfFileMerger
import os
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI

print = sg.EasyPrint


def clean(original_file, home_directory, to_directory, file_name):
    filepath = os.path.dirname(original_file)
    relative_directory = os.path.relpath(filepath, home_directory)
    output_directory = os.path.join(to_directory, relative_directory)
    output_filename = os.path.join(output_directory, file_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    merger = PdfFileMerger()
    input1 = PdfFileReader(open(original_file, "rb"))
    merger.append(input1)
    output = open(output_filename, "wb")
    merger.write(output)
    print(file_name + " metadata removed")
