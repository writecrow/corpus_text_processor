from .utils import BaseParser
import chardet
import codecs
from parsers import encoding

class Parser(BaseParser):
    """Parse ``.txt`` files"""

    def extract(self, filename):
        # Open the file so we can guess its encoding.
        rawdata = open(filename, 'rb').read()
        detected = chardet.detect(rawdata)
        encoding_method = encoding.get_encoding(detected['encoding'])
        if (encoding_method):
            with open(filename, encoding=encoding_method) as stream:
                return stream.read()
