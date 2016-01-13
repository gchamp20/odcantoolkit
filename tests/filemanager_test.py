import unittest
from odcantoolkit.filemanager import unzipfile
from os import mkdir


class filemanagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            mkdir("tests/results/")
        except FileExistsError:
            pass # silently ignore if folder already there

    def test_unzipfile(self):
        received = unzipfile("tests/ressources/filemanager/test.zip", "csv", "tests/results/")
        self.assertIn("ok1.csv", received)
        self.assertIn("ok2.csv", received)
        self.assertIn("ok3.csv", received)


if __name__ == '__main__':
    unittest.main()
