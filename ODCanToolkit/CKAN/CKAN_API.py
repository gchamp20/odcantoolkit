import urllib.request
import urllib
import json
import re


URL_REGEX = re.compile("^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$")  # credits to @stephenhay


class Request:
    """Wrapper class using urllib to make a request to a CKAN API.

    The public interface is the same as any CKAN api. Refer to the API's documentation
    to know the content of each response: docs.ckan.org/en/latest/api/index.html
    """
    def __init__(self, url):
        if URL_REGEX.match(url):
            self._url = url
        else:
            raise TypeError("API's url is not valid")

    def package_show(self, id):
        """ Returns the JSON response from the server. """

        return self._execute_action('package_show', {'id': id})

    def _execute_action(self, functionName, params=None):
        request = self._make_request_object(functionName, params)
        response = self._send_request(request)
        response = json.loads(response)
        return response

    def _make_request_object(self, functionName, params):
        paramString = ''
        for key, value in params.items():
            paramString = '{0}{1}={2}&'.format(paramString, key, value)
        url = '{0}action/{1}?{2}'.format(self._url, functionName, paramString)
        return urllib.request.Request(url)

    def _send_request(self, reqObject):
        # will throw HTTP errors!
        response = urllib.request.urlopen(reqObject)
        return response.read().decode('utf8')


class FileInfo:
    """ Data structure to hold common files attributes """

    def __init__(self, attributes_dictonary):
        self._attributes = attributes_dictonary

    def get_name(self):
        return self._attributes['name']

    def get_language(self):
        return self._attributes['language']

    def get_format(self):
        return self._attributes['format']

    def get_url(self):
        return self._attributes['url']

    def get_attribute(self, key):
        try:
            attrib = self._attributes[key]
        except KeyError:
            # should be handled differently
            raise
        return attrib

    @staticmethod
    def get_attributes_key():
        return ('name', 'language', 'format', 'url')


class ResponseParser:
    """The class gives static method used to extract informations from a
    CKAN API JSON response
    """
    def __init__(self):
        pass

    @staticmethod
    def extract_files_infos(packageShowReponse, typeFilter=None):
        """Returns a list of FileInfo objects

        Used to parse the response from a package_show request.
        typeFilter -- Set that can be used to remove some file formats.
        """

        if 'resources' not in packageShowReponse['result']:
            raise TypeError("Resources not found in this response")

        payload = []
        keys = FileInfo.get_attributes_key()

        for element in packageShowReponse['result']['resources']:
            fileData = {}
            for key in keys:
                if key in element:
                    fileData[key] = element[key]
            payload.append(FileInfo(fileData))

        if typeFilter is not None:
            payload = ResponseParser._remove_wrong_formats(payload, typeFilter)

        return payload

    @staticmethod
    def _remove_wrong_formats(payload, typeFilter):
        tempPayload = []
        for result in payload:
            if result.get_format() in typeFilter:
                tempPayload.append(result)
        return tempPayload
