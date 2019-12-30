import sys
import re
import os
import chardet
import codecs
import shutil
import string


def get_encoding(argument):
    # In the below dictionary, the key is encoding provided by the `chardet`
    # module. The value is the encoding to use from the `codecs`
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
    encoding = switcher.get(argument, False)
    if not encoding:
        # @todo: split first six characters of argument
        prefix = 'todo'
        if prefix == "UTF-16":
            encoding = 'utf-16'
        elif prefix == 'UTF-32':
            encoding = 'utf_32'
        encoding = False
    return encoding
