#!/usr/local/bin/python3
# This script remove PDF metadata
# It expects a PDF file as `original_file`
# and outputs a PDF file to the specified `destination`

from PyPDF3 import PdfFileReader, PdfFileMerger
import os
import sys


def run(original_file, source, destination, file_name, extension):
    if extension != ".pdf":
        return {'name': file_name, 'result': False, 'message': 'Not a PDF'}
    filepath = os.path.dirname(original_file)
    relative_directory = os.path.relpath(filepath, source)
    output_directory = os.path.join(destination, relative_directory)
    output_filename = os.path.join(output_directory, file_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    merger = PdfFileMerger()
    try:
        input1 = PdfFileReader(open(original_file, "rb"))
        merger.append(input1)
        output = open(output_filename, "wb")
        merger.write(output)
        return {'name': file_name, 'result': True, 'message': 'Success!'}
    except:
        message = str(sys.exc_info()[1])
        return {'name': file_name, 'result': False, 'message': message}
