from striprtf.striprtf import rtf_to_text
from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from rtf file using striprtf.
    """

    def extract(self, filename):
        with open(filename) as stream:
            return rtf_to_text(stream.read())
