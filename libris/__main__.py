"""
Builds a PDF from a JSON configuration file that points to various Markdown source files.

usage: libris <configuration_file>

Where <configuration_file> is a JSON file that specifies how to build the PDF. View the full docs
for details.
"""
import argparse
import os
import sys
import jsonschema
from .lib.constants import JSON_SCHEMA_PATH
from .lib.data_extractors import get_json_data
from .lib.pdf_builder import build_pdf
from .lib.watch import watch

def main(config_file_path: str, should_watch: bool, be_verbose: bool, skip_validation: bool):
    """
    Builds a PDF from a JSON configuration file that points to various Markdown source files.
    Optionally watches for changes.

    Args:
        config_file (str): The configuration file to be used.
        should_watch (bool): Whether to watch the source files for changes and re-compile.
        be_verbose (bool): Whether to print debugging information.
        skip_validation (bool): Whether to skip JSON validation.
    """
    try:
        config = get_config_and_validate(config_file_path, skip_validation)
    except jsonschema.exceptions.ValidationError as err:
        terminate_with_validation_error(err)
    if should_watch:
        build_pdf(config, be_verbose)
        watch(config_file_path, be_verbose)
    else:
        build_pdf(config, be_verbose)

def get_config_and_validate(config_file_path: str, skip_validation: bool) -> dict:
    """
    Retrieves the configuration file and validates against the schema.

    Args:
        config_file_path (str): Path to the configuration file.
        skip_validation (bool): Whether to skip JSON validation.

    Returns:
        dict: The validated configuration object.
    """
    config = get_json_data(config_file_path)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    schema = get_json_data(os.path.join(dir_path, JSON_SCHEMA_PATH))
    if not skip_validation:
        jsonschema.validate(config, schema)
    return config

def terminate_with_validation_error(err: jsonschema.exceptions.ValidationError):
    """
    Terminates the application with a validation error.

    Args:
        err (jsonschema.exceptions.ValidationError): The error thrown.
    """
    print(err)
    print('Error: config file format is not valid!')
    sys.exit(1)

def handle_args() -> str:
    """
    Builds an argument parser for the application

    Returns:
        str: The configuration file to be used for constructing the PDF.
    """
    parser = argparse.ArgumentParser(
        prog='libris',
        description='Builds a PDF from a JSON configuration file that points to various Markdown'\
        ' source files.'
    )
    parser.add_argument(
        'config_file',
        type=str,
        help='A JSON file that specifies how to build the PDF. View the full docs for details.'
    )
    parser.add_argument(
        '-w',
        '--watch',
        action='store_true',
        help='Watch the source files and re-compile on changes.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Prints additional logging data, including intermediate HTML.'
    )
    parser.add_argument(
        '-n',
        '--no-validation',
        action='store_true',
        help='Skips JSON validation up-front. Use if you are getting URL resolution errors.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    arguments = handle_args()
    main(arguments.config_file, arguments.watch, arguments.verbose, arguments.no_validation)
