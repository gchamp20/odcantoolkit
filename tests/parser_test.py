import unittest
from ODCanToolkit.parser.csv import CsvParser


class csvParserTestCase(unittest.TestCase):
    def test_find_header(self):
        p = CsvParser("tests/ressources/parser/OccupationalInjuries.csv")
        headers = p.find_headers()
        self.assertEqual(len(headers), 13)
        self.assertEqual(headers[0], "Industry")


if __name__ == '__main__':
    unittest.main()
