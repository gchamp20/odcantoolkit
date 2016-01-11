from canadaODPtool.parser.csv import CsvParser


class ParserFactory():
    """ Factory class to build parsers depending on the file type."""

    @staticmethod
    def build_csv_parser(filename):
        return CsvParser(filename)

    @staticmethod
    def build_parser(filetype, filename):
        if filetype.upper() == "CSV":
            return CsvParser(filename)
        else:
            raise NoParserFoundError("{0} file format is not supported".format(filetype))


class NoParserFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
