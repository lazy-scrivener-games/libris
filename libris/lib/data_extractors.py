"""
Configuration data extraction functions for libris.
"""
import json
import os
import subprocess
from typing import Union
from bs4 import BeautifulSoup
from markdown2 import markdown
from weasyprint import HTML, CSS

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

def get_default_style(default_style_key: str, css_data: dict) -> Union[list, None]:
    """
    Retrieves the default style from the CSS list.

    Args:
        default_style_key (str): The name of the default style to use.
        css_data (dict): Dictionary of friendly style names and style source files.

    Returns:
        str|list: A string or list or strings pointing to CSS files.
    """
    default_style = None
    if default_style_key and default_style_key in css_data:
        default_style = css_data[default_style_key]
    return default_style

def get_html_data(
        sources: list,
        document_wrapper_class: str,
        markdown_pipe: Union[str, None],
        be_verbose: bool
    ) -> list:
    """
    Retrieves Weasyprint HTML objects based on a list of Markdown sources

    Args:
        sources (list): List of source Markdown sources to use
        document_wrapper_class (str): Optional class in which to wrap resulting document.
        markdown_pipe (str): Transformative command to run. HTML will be passed to command as
            stdin and the command's stdout output will be used instead of the raw HTML.
        be_verbose (bool): Whether to print additional debugging information.

    Returns:
        list: List of dictionaries containing original configuration plus Weasyprint HTML objects.
    """
    output = []
    for item in sources:
        item_output = get_output_from_source(item, document_wrapper_class, markdown_pipe, be_verbose)
        output.append(item_output)
    return output

def get_output_from_source(
        item: Union[dict, str],
        document_wrapper_class: str,
        markdown_pipe: Union[str, None],
        be_verbose: bool
    ) -> dict:
    """
    Gets a source configuration dictionary from a source dictionary or string.

    Args:
        item (Union[dict, str]): Source configuration dictionary or string
        document_wrapper_class (str): Optional div class with which to wrap HTML.
        be_verbose (bool): Whether to print additional debugging information.

    Returns:
        dict: Configuration dictionary with parsed HTML.
    """
    html, item_output = get_html_from_source(item, markdown_pipe)
    if document_wrapper_class:
        html = wrap_with_tag(html, document_wrapper_class)
    if be_verbose:
        print(html)
    html_object = HTML(string=html, base_url='.')
    item_output['html'] = html_object
    return item_output

def get_html_from_source(
        item: Union[dict, str],
        markdown_pipe: Union[str, None]
    ) -> 'tuple[str, dict]':
    """
    Retrieves HTML from one or more markdown source files.

    Args:
        item (Union[dict, str]): Source configuration dictionary or string

    Returns:
        str: HTML result from one or more markdown files.
        dict: Object for storage of the files' details for later processing.
    """
    if isinstance(item, str):
        return get_html_from_string_source(item, markdown_pipe)
    if 'source' in item:
        return get_html_from_dict_with_source(item, markdown_pipe)
    if 'sources' in item:
        return get_html_from_dict_with_sources(item, markdown_pipe)
    return get_html_from_dict_with_source_directory(item, markdown_pipe)

def get_html_from_string_source(item: str, markdown_pipe: Union[str, None]) -> 'tuple[str, dict]':
    """
    Retrieves HTML from a markdown source file.

    Args:
        item (str): Source configuration string.

    Returns:
        str: HTML result from the markdown file.
        dict: Object for storage of the file's details for later processing.
    """
    with open(item, 'r') as markdown_file:
        text = markdown_file.read()
        text = apply_pipe(text, markdown_pipe)
        html = markdown(text, extras=['fenced-code-blocks', 'markdown-in-html', 'tables'])
        return html, {}

def get_html_from_dict_with_source(
        item: dict,
        markdown_pipe: Union[str, None]
    ) -> 'tuple[str, dict]':
    """
    Retrieves HTML from a markdown source file.

    Args:
        item (dict): Source configuration dictionary.

    Returns:
        str: HTML result from a markdown file.
        dict: Object for storage of the file's details for later processing.
    """
    with open(item['source'], 'r') as markdown_file:
        text = markdown_file.read()
        text = apply_pipe(text, markdown_pipe)
        html = markdown(
            text,
            extras=['fenced-code-blocks', 'markdown-in-html', 'tables']
        )
        return html, item

def get_html_from_dict_with_sources(
        item: dict,
        markdown_pipe: Union[str, None]
    ) -> 'tuple[str, dict]':
    """
    Retrieves HTML from one or more markdown source files.

    Args:
        item (dict): Source configuration dictionary.

    Returns:
        str: HTML result from one or more markdown files.
        dict: Object for storage of the files' details for later processing.
    """
    markdown_text = ''
    is_first = True
    for source in item['sources']:
        if not is_first:
            markdown_text += '\n\n'
        is_first = False
        with open(source, 'r') as markdown_file:
            file_text = markdown_file.read()
            file_text = apply_pipe(file_text, markdown_pipe)
            markdown_text += file_text
    html = markdown(markdown_text, extras=['fenced-code-blocks', 'markdown-in-html', 'tables'])
    return html, item

def get_html_from_dict_with_source_directory(
        item: dict,
        markdown_pipe: Union[str, None]
    ) -> 'tuple[str, dict]':
    """
    Retrieves HTML from a directory of markdown source files.

    Args:
        item (dict): Source configuration dictionary.

    Returns:
        str: HTML result from one or more markdown files.
        dict: Object for storage of the files' details for later processing.
    """
    markdown_text = ''
    is_first = True
    file_list = os.listdir(item['sourceDirectory'])
    file_list.sort()
    for file_entry in file_list:
        filename = os.path.join(item['sourceDirectory'], file_entry)
        if os.path.isfile(filename) and filename.lower().endswith('.md'):
            if not is_first:
                markdown_text += '\n\n'
            is_first = False
            with open(filename, 'r') as markdown_file:
                file_text = markdown_file.read()
                file_text = apply_pipe(file_text, markdown_pipe)
                markdown_text += file_text
    html = markdown(markdown_text, extras=['fenced-code-blocks', 'markdown-in-html', 'tables'])
    return html, item

def apply_pipe(markdown_text: str, pipe: Union[str, None]) -> str:
    """
    Applies a pipe command to a markdown file and returns output.

    Args:
        markdown_text (str): Markdown file to be modified.
        pipe (Union[str, None]): Pipe command, or None if no pipe.

    Returns:
        str: Piped markdown result.
    """
    if pipe is None:
        return markdown_text
    pipe_output = subprocess.check_output(pipe, input=bytearray(markdown_text, 'utf-8'))
    return pipe_output.decode('utf-8')

def wrap_with_tag(html: str, document_wrapper_class: str) -> str:
    """
    Wraps a string of HTML with a div using a given wrapper class

    Args:
        html (str): The HTML to be wrapped
        document_wrapper_class(str): The class with which to wrap the HTML

    Returns:
        str: Newly wrapped HTML
    """
    soup = BeautifulSoup(html, 'html.parser')
    new_div = soup.new_tag('div')
    new_div['class'] = document_wrapper_class
    for element in soup:
        new_div.append(element)
    return new_div.prettify()

def get_css_data(styles: dict) -> dict:
    """
    Retrieves Weasyprint CSS objects based on a dictionary of CSS filenames.

    Args:
        styles (dict): Dictionary of CSS filenames, with keys as friendly names.

    Returns:
        dict: Dictionary of lists of Weasyprint CSS objects, with keys as friendly names.
    """
    output = {}
    for key in styles:
        value = styles[key]
        output[key] = []
        if isinstance(value, str):
            css = CSS(filename=value)
            output[key].append(css)
        elif isinstance(value, list):
            output[key] = convert_list_to_css_objects(value)
        else:
            output[key] = get_css_data_from_style_object(value)
    return output

def get_css_data_from_style_object(style: dict) -> list:
    """
    Retrieves Weasyprint CSS objects based on a schema-defined style object.

    Args:
        style(dict): Schema-defined style object.

    Returns:
        list: List of Weasyprint CSS objects.
    """
    if 'stylesheet' in style:
        css = CSS(filename=style['stylesheet'])
        return [css]
    if 'stylesheets' in style:
        output = []
        for stylesheet in style['stylesheets']:
            css = CSS(filename=stylesheet)
            output.append(css)
        return output
    return []

def convert_list_to_css_objects(sources: list) -> list:
    """
    Takes a list of filenames and outputs a list of CSS objects.

    Args:
        sources(list): List of filenames for CSS files.

    Returns:
        list: List of Weasyprint CSS objects.
    """
    output = []
    for value in sources:
        css = CSS(filename=value)
        output.append(css)
    return output

def get_decorator_data_from_styles_dict(styles: dict) -> dict:
    """
    Takes a dictionary of style data objects and outputs a decorator data object.

    Args:
        styles(dict): Dictionary of schema-defined style data.

    Returns:
        dict: Dictionary of schema-defined decorator data.
    """
    output = {}
    for key in styles:
        value = styles[key]
        if isinstance(value, dict):
            output[key] = get_decorator_data_from_style(value)
    return output

def get_decorator_data_from_style(style: dict) -> list:
    """
    Takes a schema-defined style data object and outputs decorator data for that style.

    Args:
        style(dict): Schema-defined style data object

    Returns:
        list: List of decorators for that style.
    """
    output = []
    if 'decorator' in style:
        output.append(get_decorator_data(style['decorator']))
    elif 'decorators' in style:
        for decorator in style['decorators']:
            output.append(get_decorator_data(decorator))
    return output

def get_decorator_data(decorator: dict) -> dict:
    """
    Takes a schema-defined decorator object and outputs HTML and CSS data for that decorator.

    Args: decorator(dict): Schema-defined decorator object.

    Returns:
        dict: Dictionary containing 'html' and 'css' keys for that decorator.
    """
    with open(decorator['template'], 'r') as template_file:
        html = template_file.read()
    output = {
        'html': html,
        'css': CSS(filename=decorator['stylesheet'])
    }
    if 'evenStylesheet' in decorator:
        output['evenCss'] = CSS(filename=decorator['evenStylesheet'])
    if 'oddStylesheet' in decorator:
        output['oddCss'] = CSS(filename=decorator['oddStylesheet'])
    return output
