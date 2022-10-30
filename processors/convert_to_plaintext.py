#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import docx2txt
import locale
import os
import string
import sys

from parsers import docx_parser
from parsers import pdf2word_parser
from parsers import html_parser
from parsers import pptx_parser
from parsers import rtf_parser
from parsers import txt_parser
from parsers import linebreaks


os.environ["PYTHONIOENCODING"] = "utf-8"
myLocale = locale.setlocale(category=locale.LC_ALL, locale="")


def run(original_file, source, destination, file_name, extension, values):
    supported_filetypes = ['.docx', '.html', '.pdf', '.pptx', '.rtf', '.txt']
    # If the file is empty, move on.
    if os.stat(original_file).st_size == 0:
        return {'name': file_name, 'result': False, 'message': 'File is empty'}
    elif extension not in supported_filetypes:
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
            parser = pdf2word_parser.Parser()
        elif extension == ".html":
            parser = html_parser.Parser()
        elif extension == ".txt":
            parser = txt_parser.Parser()
        elif extension == ".rtf":
            parser = rtf_parser.Parser()
        # Extract the text
        if extension != ".doc":
            plaintext = parser.process(original_file, "utf_8")

        if type(plaintext) is not str:
            plaintext = plaintext.decode('utf-8')
        if values['removeLinebreaks'] is not False:
            # Remove duplicate linebreaks
            plaintext = linebreaks.remove(plaintext)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(plaintext)
        return {'name': file_name, 'result': True, 'message': 'Success!'}

    except:
        message = str(sys.exc_info()[1])
        return {'name': file_name, 'result': False, 'message': message}
