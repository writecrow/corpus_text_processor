import os
import shutil
import six
from pdf2docx import Converter
import docx2txt
from six import StringIO
import tempfile
import re

from exceptions import UnknownMethod, ShellError

from .utils import ShellParser


class Parser(ShellParser):

    def extract(self, filename):
        # convert pdf to docx
        cv = Converter(filename)
        wordfile = tempfile.NamedTemporaryFile()
        cv.convert(wordfile.name, start=0, end=None)
        cv.close()
        output = docx2txt.process(wordfile.name)

        # replace line breaks with <p>
        content = re.sub(r'\n\n+','<p>', output)
        # if <p> is followed by a lower case character
        # replace <p> with space, keep the lower case character
        content = re.sub(r'<p>([a-z])',r' \g<1>',content)
        # any <p> left is an actual line break
        content = re.sub(r'<p>',r'\n',content)

        # The following line appears to be too greedy
        #content = re.sub(r'([a-z]) \n', r'\g<1> ', content)

        return content