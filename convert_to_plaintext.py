#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files, convert to plaintext.

import sys
import os
import string
import docx2txt
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from six import StringIO
from parsers import html_parser
from parsers import pptx_parser
import PySimpleGUI as sg


# Windows can use PySimpleGUI
printable = set(string.printable)

def extract_from_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()

    return str.replace("\\n","\n")

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
            plaintext = docx2txt.process(original_file)
        elif extension == ".pdf":
            plaintext = extract_from_pdf(original_file)
        elif extension == ".html":
            parser = html_parser.Parser()
            plaintext = parser.extract(original_file)
        elif extension == ".pptx":
            parser = pptx_parser.Parser()
            plaintext = parser.extract(original_file)
        output_file = open(output_filename, "w")
        output_file.write(plaintext)
        output_file.close()
        sg.EasyPrint(name_only, ":\t\tplaintext created successfully")
    except:
        sg.EasyPrint(file_name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))
