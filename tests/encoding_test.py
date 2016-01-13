import unittest
from odcantoolkit.encoding import guessing


class guess_encodingTestCase(unittest.TestCase):
    def test_guess_encoding(self):
        # test utf_8
        encodingType = guessing.guess_encoding("tests/ressources/encoding/utf8.txt")
        self.assertEqual(encodingType, "utf_8")

        # test latin_1
        encodingType = guessing.guess_encoding("tests/ressources/encoding/latin_1.txt")
        self.assertEqual(encodingType, "latin_1")

        # test others
        encodingType = guessing.guess_encoding("tests/ressources/encoding/other.txt")
        self.assertEqual(encodingType, "utf_8")

        # couldn't create a cp863 on linux mint, should be added


if __name__ == '__main__':
    unittest.main()
