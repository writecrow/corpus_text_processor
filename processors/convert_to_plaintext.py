#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import docx2txt
import locale
import os
import string
import sys

from parsers import html_parser
from parsers import doc_parser
from parsers import docx_parser
from parsers import pdf_parser
from parsers import pptx_parser
from parsers import txt_parser

os.environ["PYTHONIOENCODING"] = "utf-8"
myLocale = locale.setlocale(category=locale.LC_ALL, locale="en_US.UTF-8")


def run(original_file, source, destination, file_name, extension):
    supported_filetypes = ['.docx', '.pdf', '.html', '.pptx', '.txt']
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
        if extension == ".pptx":
            parser = pptx_parser.Parser()
        elif extension == ".pdf":
            parser = pdf_parser.Parser()
        elif extension == ".html":
            parser = html_parser.Parser()
        elif extension == ".txt":
            parser = txt_parser.Parser()
        plaintext = parser.process(original_file, "utf_8")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(plaintext.decode('utf-8'))
        return {'name': file_name, 'result': True, 'message': 'Success!'}
    except:
        message = str(sys.exc_info()[1])
        return {'name': file_name, 'result': False, 'message': message}
