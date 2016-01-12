import unittest
from ODCanToolkit.filemanager import unzipfile
from os import mkdir


class filemanagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mkdir("tests/results/")

    def test_unzipfile(self):
        received = unzipfile("tests/ressources/filemanager/test.zip", "csv", "tests/results/")
        self.assertIn("ok1.csv", received)
        self.assertIn("ok2.csv", received)
        self.assertIn("ok3.csv", received)


if __name__ == '__main__':
    unittest.main()
