import unittest
from canadaODPtool.parser.csv import CsvParser


class csvParserTestCase(unittest.TestCase):
    def test_find_header(self):
        p = CsvParser("tests/ressources/parser/OccupationalInjuries.csv")
        headers = p.find_headers()
        self.assertEqual(len(headers), 13)
        self.assertEqual(headers[0], "Industry")

        # Checking the correct exception is raised when the headers coudn't be found
        p2 = CsvParser("tests/ressources/parser/wrong_headers.csv")
        self.assertRaises(RuntimeError, p2.find_headers)

if __name__ == '__main__':
    unittest.main()
