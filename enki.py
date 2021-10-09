"""
Builds a PDF from a JSON configuration file that points to various Markdown source files.

usage: enki.py <configuration_file>

Where <configuration_file> is a JSON file that specifies how to build the PDF. View the full docs
for details.
"""
import argparse

def main(config_file: str):
    """
    Builds a PDF from a JSON configuration file that points to various Markdown source files.

    Args:
        config_file (str): The configuration file to be used.
    """

def handle_args():
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
