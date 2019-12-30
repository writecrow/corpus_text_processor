import sys
import re
import os
import chardet
import codecs
import shutil
import string

import PySimpleGUIQt as sg
print = sg.Print


def get_encoding(argument):
    # In the below dictionary, the key is encoding provided by the `chardet` (see https://github.com/chardet/chardet).
    # module. The value is the encoding to use from the `codecs`
    # module. See
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    switcher = {
        'ASCII': 'ascii',
        'BIG5': 'big5',
        'CP932': 'cp932',
        'GB2312': 'gb2312',
        'EUC-KR': 'euc_kr',
        'EUC-JP': 'euc_jp',
        'EUC-TW': 'gb18030',
        'HZ-GB-2312': 'hz',
        'IBM855': 'cp855',
        'IBM866': 'cp866',
        'ISO-2022-CN': 'gb2312',
        'ISO-2022-JP': 'iso2022_jp',
        'ISO-2022-KR': 'iso2022_kr',
        'ISO-8859-1': 'iso8859_1',
        'ISO-8859-2': 'iso8859_2',
        'ISO-8859-5': 'iso8859_5',
        'ISO-8859-7': 'iso8859_7',
        'ISO-8859-8': 'iso8859_8',
        'KOI8-R': 'koi8_r',
        'MACCYRILLIC': 'cp1256',
        'SHIFT_JIS': 'shift_jis',
        'TIS-620': 'cp874',
        'WINDOWS-1251': 'windows-1251',
        'WINDOWS-1252': 'cp1252',
        'WINDOWS-1253': 'cp1253',
        'WINDOWS-1254': 'cp1254',
        'WINDOWS-1255': 'cp1255',
        'UTF-8-SIG': 'utf-8-sig',
        'UTF-16': 'utf-16',
        'UTF-32': 'utf_32',
    }
    encoding = switcher.get(argument.upper(), False)
    if not encoding:
        # Check for wildcard matches for UTF-16 & 32.
        prefix = argument[0:6]
        if prefix == "UTF-16":
            encoding = 'utf-16'
        elif prefix == 'UTF-32':
            encoding = 'utf_32'
    return encoding
