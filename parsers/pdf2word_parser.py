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
        return output
