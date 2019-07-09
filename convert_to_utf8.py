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
        'MacCyrillic': 'cp1256',
        'windows-1251': 'windows-1251',
        'Windows-1252': 'cp1252',
        'Windows-1254': 'cp1254',
        'UTF-8-SIG': 'utf-8-sig',
        'UTF-16': 'utf-16',
        'UTF-32': 'utf_32'
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


def convert(filename, name):
    output_filename = filename
    # Open the file so we can guess its encoding.
    rawdata = open(filename, 'rb').read()
    detected = chardet.detect(rawdata)
    encoding_method = get_encoding(detected['encoding'])
    if (encoding_method):
        u = decode(filename, encoding_method)
        out = codecs.open(output_filename, 'w', 'utf-8')
        out.write(u['file'])
        out.close()
        feedback = name + " :\t\t converted from " + u['encoding']
    else:
        try:
            shutil.copy(filename, output_filename)
        except shutil.SameFileError:
            # code when Exception occur
            pass
        else:
            # code if the exception does not occur
            pass
        finally:
            if (detected['encoding'] == 'utf-8'):
                feedback = name + ":\t\t already encoded in utf-8"
            elif detected['encoding'] == None:
                print(detected)
                feedback = name + ":\t\t encoding ambiguous" + "(No change)"
            else:
                feedback = name + ":\t\t detected as" + detected['encoding'] + "(No change)"
    print(feedback)
