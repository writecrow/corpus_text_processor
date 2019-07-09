#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import sys
import re
import os
import chardet
import codecs
import shutil
import string
import textract
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI

printable = set(string.printable)


def convert(original_file, home_directory, file_name):
    try:
        base_directory = os.path.join(home_directory, "plaintext")
        filepath = os.path.dirname(original_file)
        relative_directory = os.path.relpath(filepath, home_directory)
        output_directory = os.path.join(base_directory, relative_directory)
        name_only = os.path.splitext(file_name)[0]
        output_filename = os.path.join(output_directory, name_only)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        plaintext = textract.process(original_file)
        output_file = open(output_filename, "w")
        output_file.write(plaintext.decode('utf-8'))
        output_file.close()
        sg.EasyPrint(name_only, ":\t\tplaintext created successfully")
    except:
        sg.EasyPrint(file_name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))
