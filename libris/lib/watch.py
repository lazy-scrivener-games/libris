"""
Watch functionality for libris.
"""
import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .data_extractors import get_json_data
from .pdf_builder import build_pdf

class WatchEventHandler(FileSystemEventHandler):
    """
    Event handler for the watch function.
    """
    def __init__(self, config_path: str, be_verbose: bool):
        self.config_path = config_path
        self.be_verbose = be_verbose
        super().__init__()

    def on_any_event(self, event):
        """
        Runs on any file event in the watched directories.
        """
        print('Files changed, recompiling...')
        config = get_json_data(self.config_path)
        build_pdf(config, self.be_verbose)

def watch(config_file_path: str, be_verbose: bool):
    """
    Watches the config file and all referenced files and re-builds the PDF whenever they change.

    Args:
        config_file_path (str): The configuration file path.
        be_verbose (bool): Whether to print debugging information.
    """
    observer = Observer()
    handler = WatchEventHandler(config_file_path, be_verbose)
    try:
        while True:
            observer = watch_loop_iteration(observer, handler, config_file_path)
    finally:
        observer.stop()
        observer.join()

def watch_loop_iteration(
        observer: Observer,
        handler: WatchEventHandler,
        config_file_path: str
    ) -> Observer:
    """
    A single iteration of the watch loop.

    Args:
        observer (Observer): Last constructed file system observer.
        handler (WatchEventHandler): Event handler for file system changes.
        config_file_path (str): The path to the configuration file. 
    """
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
    """
    Creates a list of files to watch from the configuration file.

    Args:
        config_file_path (str): The path to the configuration file.

    Returns:
        list: A list of filenames to be watched.
    """
    config = get_json_data(config_file_path)
    file_list = [config_file_path]
    add_string_or_string_collection_if_present(file_list, config['sources'], ['source'])
    if 'styles' in config:
        for key in config['styles']:
            value = config['styles'][key]
            add_string_or_string_collection_if_present(
                file_list,
                value,
                [
                    'stylesheet',
                    'stylesheets',
                    'decorator',
                    'template',
                    'oddStylesheet',
                    'evenStylesheet',
                    'decorators'
                ]
            )
    return file_list

def add_string_or_string_collection_if_present(list_to_add_to: list, item: any, subkeys: list):
    """
    Recursively adds a string or collection of strings (or collection of collections of strings,
    etc.) to a list. Only checks specified subkeys.

    Args:
        list_to_add_to (list): The list to which to append located strings.
        item (any): The object to check. Objects other than strings, dictionaries, and lists will
            not be processed.
        subkeys (list): List of strings which are the keys to check in located dictionaries.
    """
    if isinstance(item, str):
        list_to_add_to.append(item)
    elif isinstance(item, dict):
        for subkey in subkeys:
            if subkey in item:
                add_string_or_string_collection_if_present(list_to_add_to, item[subkey], subkeys)
    elif isinstance(item, list):
        for subitem in item:
            add_string_or_string_collection_if_present(list_to_add_to, subitem, subkeys)

def convert_file_list_to_directories(file_list: list) -> list:
    """
    Takes a list of relative file paths and converts to absolute directory paths, making sure all
    results are unique.

    Args:
        file_list (list): List of relative file paths to process.

    Returns:
        list: List of unique absolute directory paths containing all files from file_list.
    """
    output = []
    for filename in file_list:
        output.append(os.path.dirname(os.path.abspath(filename)))
    return list(set(output))
