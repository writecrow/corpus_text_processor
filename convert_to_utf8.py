#!/usr/local/bin/python3

# DESCRIPTION: Given a file or files passed as arguments to the script,
# attempt to guess the character encoding and open each file as such.
# If that fails, try to open the file as.
# Finally, encode the file in utf8 and place it in an "output" directory

import argparse
import chardet
import codecs
import os
import shutil
import sys
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI

print = sg.EasyPrint


def get_encoding(argument):
    # In the below dictionary, the key is encoding provided by the chardet
    # module. The value is the encoding to use from the codecs
    # module. See
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    switcher = {
        'ascii': 'ascii',
        'ISO-8859-1': 'utf-8-sig',
        'ISO-8859-2': 'utf-8-sig',
        'MacCyrillic': 'cp1256',
        'windows-1251': 'windows-1251',
        'Windows-1252': 'cp1252',
        'Windows-1254': 'cp1254',
        'UTF-8-SIG': 'utf-8-sig',
        'UTF-16': 'utf-16',
        'UTF-16BE': 'utf-16',
        'UTF-16LE': 'utf-16',
        'UTF-32': 'utf_32',
        'UTF-32LE': 'utf_32'
    }
    return switcher.get(argument, False)


def decode(filename, encoding_method):
    try:
        f = codecs.open(filename, 'r', encoding_method)
        return {'file': f.read(), 'encoding': encoding_method}
    except UnicodeDecodeError:
        pass
    f = codecs.open(filename, 'r', 'latin_1')
    return {'file': f.read(), 'encoding': 'latin_1'}


def convert(filename, home_directory, to_directory, name, extension):
    if extension != ".txt":
        return {'name': name, 'result': False, 'message': 'Not a .txt file'}
    try:
        filepath = os.path.dirname(filename)
        relative_directory = os.path.relpath(filepath, home_directory)
        output_directory = os.path.join(to_directory, relative_directory)
        output_filename = os.path.join(output_directory, name)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        # Open the file so we can guess its encoding.
        rawdata = open(filename, 'rb').read()
        detected = chardet.detect(rawdata)
        encoding_method = get_encoding(detected['encoding'])
        if (encoding_method):
            u = decode(filename, encoding_method)
            out = codecs.open(output_filename, 'w', 'utf-8')
            out.write(u['file'])
            out.close()
            feedback = "Converted from " + u['encoding']
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
