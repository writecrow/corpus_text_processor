import os
import shutil
import six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from six import StringIO
from tempfile import mkdtemp

from exceptions import UnknownMethod, ShellError

from .utils import ShellParser


class Parser(ShellParser):
    def extract(self, filename):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=0, password="", caching=True, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str.replace("\\n", "\n")
