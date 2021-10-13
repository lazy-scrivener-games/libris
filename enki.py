"""
Builds a PDF from a JSON configuration file that points to various Markdown source files.

usage: enki.py <configuration_file>

Where <configuration_file> is a JSON file that specifies how to build the PDF. View the full docs
for details.
"""
import argparse
import json
import os
import sys
import time
import jsonschema
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from lib.constants import JSON_SCHEMA_PATH
from lib.pdf_builder import build_pdf

def main(config_file_path: str, should_watch: bool):
    """
    Builds a PDF from a JSON configuration file that points to various Markdown source files.
    Optionally watches for changes.

    Args:
        config_file (str): The configuration file to be used.
        should_watch (bool): Whether to watch the source files for changes and re-compile.
    """
    try:
        config = get_config_and_validate(config_file_path)
    except jsonschema.exceptions.ValidationError as err:
        terminate_with_validation_error(err)
    if should_watch:
        build_pdf(config)
        watch(config_file_path)
    else:
        build_pdf(config)

def get_config_and_validate(config_file_path: str) -> dict:
    config = get_json_data(config_file_path)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    schema = get_json_data(os.path.join(dir_path, JSON_SCHEMA_PATH))
    jsonschema.validate(config, schema)
    return config

def terminate_with_validation_error(err: jsonschema.exceptions.ValidationError):
    print(err)
    print('Error: config file format is not valid!')
    sys.exit(1)
class WatchEventHandler(FileSystemEventHandler):
    def __init__(self, config_path: str):
        self.config_path = config_path
        super().__init__()

    def on_any_event(self, event):
        print('Files changed, recompiling...')
        config = get_json_data(self.config_path)
        build_pdf(config)

def watch(config_file_path: str):
    """
    Watches the config file and all referenced files and re-builds the PDF whenever they change.

    Args:
        config_file_path (str): The configuration file path.
    """
    observer = Observer()
    handler = WatchEventHandler(config_file_path)
    try:
        while True:
            observer = watch_loop_iteration(observer, handler, config_file_path)
    finally:
        observer.stop()
        observer.join()

def watch_loop_iteration(observer, handler, config_file_path) -> Observer:
    file_list = build_watch_file_list(config_file_path)
    directory_list = convert_file_list_to_directories(file_list)
    observer.unschedule_all()
    observer.stop()
    observer = Observer()
    for watched_directory in directory_list:
        observer.schedule(handler, watched_directory)
    observer.start()
    time.sleep(1)
    return observer


def build_watch_file_list(config_file_path: str) -> list:
    config = get_json_data(config_file_path)
    file_list = [config_file_path]
    for source in config['sources']:
        if isinstance(source, str):
            file_list.append(source)
        else:
            file_list.append(source['source'])
    if 'styles' in config:
        for key in config['styles']:
            style = config['styles'][key]
            if isinstance(style, str):
                file_list.append(style)
            else:
                if 'stylesheet' in style:
                    file_list.append(style['stylesheet'])
                elif 'stylesheets' in style:
                    for stylesheet in style['stylesheets']:
                        file_list.append(stylesheet)
                if 'decorator' in style:
                    decorator = style['decorator']
                    if 'template' in decorator:
                        file_list.append(decorator['template'])
                    if 'stylesheet' in decorator:
                        file_list.append(decorator['stylesheet'])
                    if 'oddStylesheet' in decorator:
                        file_list.append(decorator['oddStylesheet'])
                    if 'evenStylesheet' in decorator:
                        file_list.append(decorator['evenStylesheet'])
                elif 'decorators' in style:
                    for decorator in style['decorators']:
                        if 'template' in decorator:
                            file_list.append(decorator['template'])
                        if 'stylesheet' in decorator:
                            file_list.append(decorator['stylesheet'])
                        if 'oddStylesheet' in decorator:
                            file_list.append(decorator['oddStylesheet'])
                        if 'evenStylesheet' in decorator:
                            file_list.append(decorator['evenStylesheet'])
    return file_list

def convert_file_list_to_directories(file_list: list) -> list:
    output = []
    for filename in file_list:
        output.append(os.path.dirname(os.path.abspath(filename)))
    return list(set(output))

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
    parser.add_argument(
        '--watch',
        '-w',
        action='store_true',
        help='Watch the source files and re-compile on changes.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    arguments = handle_args()
    main(arguments.config_file, arguments.watch)
