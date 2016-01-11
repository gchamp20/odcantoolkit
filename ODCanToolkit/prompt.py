import argparse
import urllib
from ODCanToolkit.CKAN import CKAN_API
from ODCanToolkit.output.generation import JSONMaker
from ODCanToolkit.parser.factory import ParserFactory
from ODCanToolkit.parser.factory import NoParserFoundError
from ODCanToolkit.database.mongodb import IMongoDB
from pymongo.errors import ServerSelectionTimeoutError
from bson.errors import InvalidDocument
from csv import Error
import json
import re
import zipfile

def init_common_cli_arguments():
    """Inits command line arugments for the script
    Returns argparser object
    """
    argParser = argparse.ArgumentParser()
    argParser.add_argument("id", help="ID to fetch from open.canada.ca")
    argParser.add_argument("--fileformat", nargs='+',
                           help="File formats to fetch. Default is CSV only")
    return argParser


def get_cli_json_arguments():
    """Returns the command line arguments list."""
    argParser = init_common_cli_arguments()
    return argParser.parse_args()


def get_cli_mongodb_arguments():
    """Returns the command line arguments lists.

    Also set specicfs arugments for mongodb mode.
    """
    argParser = init_common_cli_arguments()
    argParser.add_argument("--dbname", help="Database name. Default is db",
                           default="db")
    argParser.add_argument("--collection", help="Collection name. Default is ckan",
                           default="ckan")
    argParser.add_argument("--host", help="Database url. Default is localhost",
                           default="localhost")
    argParser.add_argument("--port", help="Database port. Default is 27017",
                           default=27017, type=int)
    return argParser.parse_args()


def printChoices(files):
    """Returns the choosen fileInfo object.

    files -- CKAN_API.FileInfo object list
    """
    print("\nChoose wich file to download: ")
    print("Warning: English versions should be prefered due to parsing issues.\n")
    limit = len(files)
    for i in range(0, limit):
        print("\t {0}. {1} ( {2} ) : {3}".format(i+1, files[i].get_name(),
                                                  files[i].get_language(),
                                                  files[i].get_format()))
    print("")
    (choice, quit) = (None, False)
    while quit is False and choice is None:
        choice = input("Enter file number to download (or q to quit): ")
        if choice.lower() == 'q':
            quit = True
        else:
            try:
                choice = int(choice)
                assert(choice > 0 and choice <= limit)
            except:
                print("Invalid choice.")
                choice = None
    return None if quit else files[choice - 1]

def unzipfile(filename, targetformat):
    """Returns name of the unzipped file

    Unzip a file and looks for the file matching the targetformat
    filename -- Name of the file (str)
    targetformat -- Format to extract from the archive (CSV, HTML, etc)
    """
    zip_ref = zipfile.ZipFile(filename, 'r')
    content = zip_ref.namelist()
    name = None
    for f in content:
        f_format = f.split('.')[1]
        if f_format.upper() == targetformat.upper():
            name = f
            break
    zip_ref.extract(name)
    zip_ref.close()
    return f

def download(choice):
    """ Returns downloaded file's name

    choice -- CKAN_API.FileInfo object to download
    """
    print("\nDownloading requested file...")
    (name, fileformat, url) = (choice.get_name(),
                               choice.get_format(),
                               choice.get_url())
    extension = url.split('.')
    extension = extension[len(extension) - 1]

    name = name.replace(' ', '_').replace(',', '') + '.' + extension
    urllib.request.urlretrieve(url, name)
    print("Download successful.")

    if extension.upper() != fileformat.upper():
        if extension == "zip":
            print("The file will be extracted from the zip archive.")
            name = unzipfile(name, fileformat)
        else:
            print("Warning: The file format seems to be {0} and not {1}".format(extension, fileformat) +
                  " (data wrongly labeled).")
    return name


def make_api_request(id, fileformat):
    """ Returns CKAN_API.FileInfo object list

    Uses CKAN_API module to send a package_show request and parse
    the anwser.
    id -- Package ID
    fileformat -- Fileformat to fetch
    """
    if fileformat is None:
        fileformat = ["CSV"]
    api = CKAN_API.Request("http://open.canada.ca/data/en/api/3/")
    PACKAGE_ID_REGEX = re.compile("^(\w+-?)+$")

    if not PACKAGE_ID_REGEX.match(id):
        raise RuntimeError("Wrong package ID format.")

    print("Sending request to open.canada.ca... ")
    metadata = api.package_show(id)
    fileFilter = {x.upper() for x in fileformat}
    fileInfos = CKAN_API.ResponseParser.extract_files_infos(metadata, fileFilter)
    return fileInfos


def make_parser(fileformat, filename):
    """ Returns parser for the specified fileofmrat

    fileformat -- Format of the parsed file.
    filename -- Name of the parsed file.
    """
    parser = ParserFactory.build_parser(fileformat,
                                        filename)
    return parser


def mongodb_mode(jsonmaker, args):
    """Build JSON and send data to the database

    jsonmaker -- JSONMaker object to extract json data from
    args -- CLI arguments containing database connection information
    """
    (host, port, dbname, collection) = (args.host,
                                        args.port,
                                        args.dbname,
                                        args.collection)
    db = IMongoDB(dbname, collection, host, port)  # could throw
    data = jsonmaker.make_json_dictionary()
    try:
        db.insert(data)
    except ServerSelectionTimeoutError:
        print("Cannot reach the database. Make sure MongoDB is up and running.")
        return
    except InvalidDocument as err:
        print("The JSON produced is not formatted correctly. ")
        print(err)
    except:
        print("Unknown error while trying to reach the database.")
        return
    print("The data was successfully inserted the database.")


def json_mode(jsonmaker, filename):
    """Builds JSON and outputs it to a file

    jsonmaker -- JSONMaker object to extract json data from
    filename -- Name of the output file
    """
    jsonData = jsonmaker.jsonify()
    with open(filename + ".json", 'w') as outfile:
        json.dump(jsonData, outfile)
    print("{0} successfully created.".format(filename + ".json"))


def main(jsonmode):
    if jsonmode:
        args = get_cli_json_arguments()
    else:
        args = get_cli_mongodb_arguments()

    try:
        fileInfos = make_api_request(args.id, args.fileformat)
    except urllib.error.HTTPError as err:
        print("The requested package is not currently available ({0})".format(err))
        return
    except urllib.error.URLError as err:
        print("Coudn't reach the webserver. Verify internet connection. ".format(err))
        return
    except RuntimeError:
        print("The ID is not valid.")
        return

    if len(fileInfos) <= 0:
        print("Couldn't find any files matching the format requierements.")
        return

    choosenFile = printChoices(fileInfos)
    if choosenFile is None:
        return

    filename = download(choosenFile)

    try:
        parser = make_parser(choosenFile.get_format(), filename)
    except NoParserFoundError as err:
        print("Cannot parse the selected file format.")
        return
    except:
        print("Cannot parse the selected file. Please manually verify this file's content.")
        return
    try:
        jsonmaker = JSONMaker(parser)
    except Error:
        print("Cannot parse the selected file. Please manually verify this file's content.")
        return

    jsonFileName = filename.replace(choosenFile.get_format(), "json")
    json_mode(jsonmaker, jsonFileName) if jsonmode else mongodb_mode(jsonmaker, args)
