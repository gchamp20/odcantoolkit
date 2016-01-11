import unittest
from ODCanToolkit.output.generation import JSONMaker
from ODCanToolkit.parser.csv import CsvParser


class JSONMakerTestCase(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, JSONMaker, "wrong class object")

    def test_make_dictionary_json(self):
        csvparser = CsvParser("tests/ressources/jsonMaker/goodFormat.csv")
        jsonmaker = JSONMaker(csvparser)
        jsonData = jsonmaker.make_json_dictionary()
        self.assertEqual(jsonData[0]['string'], "l1")
        self.assertEqual(jsonData[0]['int'], 22)
        self.assertEqual(jsonData[0]['float'], 23.0)
        self.assertEqual(jsonData[0]['en money'], 453345.0)
        self.assertEqual(jsonData[0]['fr money'], 453345.0)
        self.assertEqual(jsonData[1]['int'], -54)
        self.assertEqual(jsonData[1]['float'], -23.45)
        self.assertEqual(jsonData[2]['int'], 2224432)
if __name__ == '__main__':
    unittest.main()
