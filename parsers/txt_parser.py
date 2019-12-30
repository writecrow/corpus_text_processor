from .utils import BaseParser


class Parser(BaseParser):
    """Parse ``.txt`` files"""

    def extract(self, filename):
        with open(filename) as stream:
            return stream.read()
