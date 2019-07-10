#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import sys
import os
import string
import docx2txt
from parsers import html_parser
from parsers import doc_parser
from parsers import docx_parser
from parsers import pdf_parser
from parsers import pptx_parser
from parsers import txt_parser
import PySimpleGUIQt as sg
import locale
os.environ["PYTHONIOENCODING"] = "utf-8"
myLocale = locale.setlocale(category=locale.LC_ALL, locale="en_US.UTF-8")


# Windows can use PySimpleGUI
printable = set(string.printable)


def convert(original_file, home_directory, file_name, extension):
    try:
        base_directory = os.path.join(home_directory, "plaintext")
        filepath = os.path.dirname(original_file)
        relative_directory = os.path.relpath(filepath, home_directory)
        output_directory = os.path.join(base_directory, relative_directory)
        name_only = os.path.splitext(file_name)[0]
        output_filename = os.path.join(output_directory, name_only)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        if extension == ".docx":
            parser = docx_parser.Parser()
        if extension == ".pptx":
            parser = pptx_parser.Parser()
        elif extension == ".pdf":
            parser = pdf_parser.Parser()
        elif extension == ".html":
            parser = html_parser.Parser()
        elif extension == ".doc":
            parser = doc_parser.Parser()
        elif extension == ".txt":
            parser = txt_parser.Parser()
        plaintext = parser.process(original_file, "utf_8")
        output_file = open(output_filename, "w")
        output_file.write(plaintext.decode('utf-8'))
        output_file.close()
        sg.EasyPrint(name_only, ":\t\tplaintext created successfully")
    except:
        sg.EasyPrint(file_name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))
