"""
Builds a PDF from a JSON configuration file that points to various Markdown source files.

usage: enki.py <configuration_file>

Where <configuration_file> is a JSON file that specifies how to build the PDF. View the full docs
for details.
"""
import argparse
import json
import jsonschema
from lib.constants import JSON_SCHEMA_PATH
from lib.pdf_builder import build_pdf

def main(config_file_path: str) -> None:
    """
    Builds a PDF from a JSON configuration file that points to various Markdown source files.

    Args:
        config_file (str): The configuration file to be used.
    """
    try:
        config = get_json_data(config_file_path)
        schema = get_json_data(JSON_SCHEMA_PATH)
        jsonschema.validate(config, schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        print('Error: config file format is not valid!')
    build_pdf(config)

def get_json_data(json_file_path: str) -> dict:
    """
    Retrieves JSON from the given file.

    Args:
        json_file_path (str): The JSON file to read.

    Returns:
        dict: Dictionary representation of JSON file.
    """
    with open(json_file_path, 'r') as json_file:
        json_string = json_file.read()
        json_object = json.loads(json_string)
        return json_object

def handle_args() -> str:
    """
    Builds an argument parser for the application

    Returns:
        str: The configuration file to be used for constructing the PDF.
    """
    parser = argparse.ArgumentParser(
        description='Builds a PDF from a JSON configuration file that points to various Markdown'\
        'source files.'
    )
    parser.add_argument(
        'config_file',
        type=str,
        help='A JSON file that specifies how to build the PDF. View the full docs for details.'
    )
    return parser.parse_args().config_file

if __name__ == '__main__':
    argument = handle_args()
    main(argument)
