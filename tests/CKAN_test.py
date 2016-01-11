import unittest
import json
from canadaODPtool.CKAN import CKAN_API
from canadaODPtool.CKAN.CKAN_API import ResponseParser
from urllib import error


class ResquestTestCase(unittest.TestCase):
    def test_package_show(self):
        api = CKAN_API.Request("http://open.canada.ca/data/en/api/3/")
        jsonResponse = api.package_show("bcf66dd4-a8c0-495c-9ed4-814bb917510c")
        self.assertTrue(jsonResponse['success'])
        self.assertRaises(error.HTTPError, api.package_show, "nope")

    def test_init(self):
        self.assertRaises(TypeError, CKAN_API.Request, "blablabla")


class FileInfoTestCase(unittest.TestCase):
    def test_constructor(self):
        obj = CKAN_API.FileInfo({
            'name': "Is a name -",
            'language': "fr;en",
            'format': "CSV",
            'url': "http://test.com"
        })
        self.assertEqual(obj.get_name(), "Is a name -")
        self.assertEqual(obj.get_language(), "fr;en")
        self.assertEqual(obj.get_format(), "CSV")
        self.assertEqual(obj.get_url(), "http://test.com")


class ResponseParserTestCase(unittest.TestCase):
    def test_extract_files_infos(self):
            with open("tests/ressources/CKAN/package_show_response.json") as f:
                # test without filter
                jsonObj = json.load(f)
                infos = ResponseParser.extract_files_infos(jsonObj)
                self.assertEqual(len(infos), 4)
                self.assertEqual(infos[0].get_format(), "CSV")

                # test with filter
                infos = ResponseParser.extract_files_infos(jsonObj, {"CSV"})
                self.assertEqual(len(infos), 2)
                self.assertEqual(infos[0].get_format(), "CSV")

                # test with non existent filter
                infos = ResponseParser.extract_files_infos(jsonObj, {"PPT"})
                self.assertEqual(len(infos), 0)

if __name__ == '__main__':
    unittest.main()
