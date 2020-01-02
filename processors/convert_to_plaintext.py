#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import docx2txt
import locale
import os
import string
import sys
import win32com.client as win32
from win32com.client import constants

from parsers import html_parser
from parsers import docx_parser
from parsers import pdf_parser
from parsers import pptx_parser
from parsers import txt_parser


os.environ["PYTHONIOENCODING"] = "utf-8"
myLocale = locale.setlocale(category=locale.LC_ALL, locale="")


def run(original_file, source, destination, file_name, extension):
    supported_filetypes = ['.docx', '.pdf', '.html', '.pptx', '.txt', '.doc']
    if extension not in supported_filetypes:
        return {'name': file_name, 'result': False, 'message': 'Unsupported file type'}
    try:
        filepath = os.path.dirname(original_file)
        relative_directory = os.path.relpath(filepath, source)
        output_directory = os.path.join(destination, relative_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        name_only = os.path.splitext(file_name)[0]
        output_filename = os.path.join(destination, relative_directory, name_only + '.txt')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        if extension == ".docx":
            parser = docx_parser.Parser()
        if extension == ".doc":
            docx_filename = os.path.join(destination, relative_directory, name_only + '.docx')
            save_as_docx(original_file, docx_filename)
            parser = docx_parser.Parser()
            plaintext = parser.process(docx_filename, "utf_8")
            # Delete the temporary file.
            os.remove(docx_filename)
        if extension == ".pptx":
            parser = pptx_parser.Parser()
        elif extension == ".pdf":
            parser = pdf_parser.Parser()
        elif extension == ".html":
            parser = html_parser.Parser()
        elif extension == ".txt":
            parser = txt_parser.Parser()
        # Extract the text
        if extension != ".doc":
            plaintext = parser.process(original_file, "utf_8")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(plaintext.decode('utf-8'))
        return {'name': file_name, 'result': True, 'message': 'Success!'}

    except:
        message = str(sys.exc_info()[1])
        return {'name': file_name, 'result': False, 'message': message}

def save_as_docx(filename, destination):
    # See https://stackoverflow.com/a/57092098
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Documents.Open(filename)
    word.ActiveDocument.ActiveWindow.View.Type = 3
    word.ActiveDocument.SaveAs(
        destination, FileFormat=constants.wdFormatXMLDocument
    )
    word.Quit()