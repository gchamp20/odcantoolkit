import argparse


def init_common_arguments():
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
    argParser = init_common_arguments()
    return argParser.parse_args()


def get_cli_mongodb_arguments():
    """Returns the command line arguments lists.

    Also set specicfs arugments for mongodb mode.
    """
    argParser = init_common_arguments()
    argParser.add_argument("--dbname", help="Database name. Default is db",
                           default="db")
    argParser.add_argument("--collection", help="Collection name. Default is ckan",
                           default="ckan")
    argParser.add_argument("--host", help="Database url. Default is localhost",
                           default="localhost")
    argParser.add_argument("--port", help="Database port. Default is 27017",
                           default=27017, type=int)
    return argParser.parse_args()
