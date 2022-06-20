#!/usr/local/bin/python3

# DESCRIPTION: Given a text file passed as argument to the script,
# attempt to guess the character encoding and open each file as such.
# If that fails, open the file as `latin_1`.
# Finally, encode the file in utf8 and place it in an "output" directory

import argparse
import chardet
import codecs
from parsers import encoding
import os
import shutil
import sys


def decode(filename, encoding_method):
    try:
        f = codecs.open(filename, 'r', encoding_method)
        return {'file': f.read(), 'encoding': encoding_method}
    except UnicodeDecodeError:
        pass
    f = codecs.open(filename, 'r', 'latin_1')
    return {'file': f.read(), 'encoding': 'latin_1'}


def run(filename, source, destination, name, extension):
    if extension not in ['.html', '.txt', '.xml']:
        return {'name': name, 'result': False, 'message': 'Not a .txt file'}
    try:
        filepath = os.path.dirname(filename)
        relative_directory = os.path.relpath(filepath, source)
        output_directory = os.path.join(destination, relative_directory)
        output_filename = os.path.join(output_directory, name)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        # If the file is empty, move on.
        if os.stat(filename).st_size == 0:
            return {'name': name, 'result': False, 'message': 'File is empty'}
        # Open the file so we can guess its encoding.
        rawdata = open(filename, 'rb').read()
        detected = chardet.detect(rawdata)
        encoding_method = encoding.get_encoding(detected['encoding'])
        if (encoding_method):
            u = decode(filename, encoding_method)
            out = codecs.open(output_filename, 'w', 'utf-8')
            out.write(u['file'])
            out.close()
            feedback = "Converted from " + u['encoding']
            if u['encoding'] == 'ascii':
                feedback = "Already encoded in utf-8"
        else:
            try:
                shutil.copy(filename, output_filename)
            except shutil.SameFileError:
                return {'name': name, 'result': False, 'message': 'File exists in destination'}
            else:
                # code if the exception does not occur
                pass
            finally:
                if (detected['encoding'] == 'utf-8'):
                    feedback = "Already encoded in utf-8"
                elif detected['encoding'] is None:
                    feedback = "Encoding ambiguous (No change)"
                else:
                    feedback = "Detected as " + detected['encoding'] + " (No change)"
        return {'name': name, 'result': True, 'message': feedback}
    except:
        message = str(sys.exc_info()[1])
        return {'name': name, 'result': False, 'message': message}
