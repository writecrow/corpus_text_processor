#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files passed as arguments to the script,
# find-replace the listed characters.

import sys
import re
import os
import chardet
import codecs
import shutil
import string
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI

printable = set(string.printable)

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


def normalize(original_file, home_directory, to_directory, file_name):
    if extension != ".txt":
        return {'name': name, 'result': False, 'message': 'Not a .txt file'}
    rawdata = open(original_file, 'rb').read()
    detected = chardet.detect(rawdata)
    encoding_method = get_encoding(detected['encoding'])
    if not encoding_method:
        encoding_method = 'utf8'
    with codecs.open(original_file, 'r', encoding=encoding_method) as f:
        try:
            filepath = os.path.dirname(original_file)
            relative_directory = os.path.relpath(filepath, home_directory)
            output_directory = os.path.join(to_directory, relative_directory)
            output_filename = os.path.join(output_directory, file_name)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            # create a new file with that name, "w" is for writable
            output_file = open(output_filename, "w")
            # for each line in this file
            for line in f:
                # replace tabs with <tab>
                line = re.sub(r'\t', '<tab>', line)
                # replace smart quotes with regular quotes
                line = line.replace(u'\u2018', u"'")
                line = line.replace(u'\u2019', u"'")
                line = line.replace(u'\u201a', u"'")
                line = line.replace(u'\u201b', u"'")
                line = line.replace(u'\u201c', u'"')
                line = line.replace(u'\u201d', u'"')
                line = line.replace(u'\u201e', u'"')
                line = line.replace(u'\u201f', u'"')
                line = line.replace(u'\u2032', u"'")
                line = line.replace(u'\u2035', u"'")
                line = line.replace(u'\u2033', u'"')
                line = line.replace(u'\u2034', u'"')
                line = line.replace(u'\u2036', u'"')
                line = line.replace(u'\u2037', u'"')
                # replace i with diacritics with quotes
                line = line.replace('ì', u'"')
                line = line.replace('í', u'"')
                # replace ellipsis with single period
                line = line.replace(u'\u2024', u'.')
                line = line.replace(u'\u2025', u'.')
                line = line.replace(u'\u2026', u'.')
                # replace Armenian apostophre with regular apostophre
                line = line.replace(u'\u055a', u"'")
                # replace inverted question mark with nothing
                line = line.replace(u'\u00bf', u' ')
                # replace all dashes with regular hifen
                line = line.replace(u'\u2010', u'-')
                line = line.replace(u'\u2011', u'-')
                line = line.replace(u'\u2012', u'-')
                line = line.replace(u'\u2013', u'-')
                line = line.replace(u'\u2014', u'-')
                line = line.replace(u'\u2015', u'-')
                # sentence normalization
                line = re.sub(r'([\.\?;:])([A-Z][a-z]+)', '\g<1> \g<2>', line)
                line = re.sub(r'([,;:])([a-z][a-z]+)', '\g<1> \g<2>', line)
                line = re.sub(r'([a-z])([A-Z])', '\g<1> \g<2>', line)
                line = re.sub(r'([\.\?;:])([0-9]+\s+)', '\g<1> \g<2>', line)
                # line = re.sub(r'\r',' ', line)
                line = re.sub(r'([a-z])(\n[A-Z])', '\g<1>. \g<2>', line)
                # flatten diacritics
                line = re.sub(r'[áàãäâåāăąǎȃȧ]', 'a', line)
                line = re.sub(r'[ÁÀÃÄÂÅĀĂĄǍȂȦ]', 'A', line)
                line = re.sub(r'[éèêëēĕėęěȇ]', 'e', line)
                line = re.sub(r'[ÉÈÊËĒĔĖĘĚȆ]', 'E', line)
                line = re.sub(r'[íìîïīĭįǐȋ]', 'i', line)
                line = re.sub(r'[ÍÌÎÏĪĬĮİǏȊ]', 'I', line)
                line = re.sub(r'[øóòöõôȏȯ]', 'o', line)
                line = re.sub(r'[ØÓÒÖÕÔȎȮ]', 'O', line)
                line = re.sub(r'[úùüûǔȗ]', 'u', line)
                line = re.sub(r'[ÚÙÜÛǓȖ]', 'U', line)
                line = re.sub(r'[ÝȲ]', 'Y', line)
                line = re.sub(r'[ýÿȳ]', 'y', line)
                line = re.sub(r'œ', 'oe', line)
                line = re.sub(r'æ', 'ae', line)
                line = re.sub(r'Æ', 'AE', line)
                line = re.sub(r'[çćĉċč]', 'c', line)
                line = re.sub(r'[ÇĆĈĊČ]', 'C', line)
                line = re.sub(r'ñ', 'n', line)
                line = re.sub(r'Ñ', 'N', line)
                # use a regular expression to find non-english characters and
                # replace them with space
                # capture any name that is written in different scripts
                line = re.sub(r'[^\x00-\x7F]+', ' ', line)
                # get rid of weird line breaks (this does not seem to be working)
                line = re.sub(r'([a-z]+)\s*\n\s*([a-z]+)', '\g<1> \g<2>', line)
                # get rid of all double spaces
                line = re.sub(r'\s+', ' ', line)
                #print(line)
                # get rid space in the beginning of a line
                line = line.strip()
                # re-add tab
                line = re.sub(r'<tab>', '\t', line)
                # write our text in the file
                output_file.write(line + "\r\n")
                #print(line, file=output_file)
            # be polite and close the file
            output_file.close()
            sg.EasyPrint(file_name, ":\t\tnormalized successfully")
        except:
           sg.EasyPrint(file_name + "\t" + str(sys.exc_info()
                                              [0]) + "\t" + str(sys.exc_info()[1]))
