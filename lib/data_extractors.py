"""
Configuration data extraction functions for Enki.
"""
from bs4 import BeautifulSoup
from markdown2 import markdown_path
from weasyprint import HTML, CSS

def get_default_style(default_style_key: str, css_data: dict) -> any:
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

def get_html_data(sources: list, document_wrapper_class: str) -> list:
    """
    Retrieves Weasyprint HTML objects based on a list of Markdown filenames

    Args:
        sources (list): List of source Markdown files to use
        document_wrapper_class (str): Optional class in which to wrap resulting document.

    Returns:
        list: List of dictionaries containing original configuration plus Weasyprint HTML objects.
    """
    output = []
    for item in sources:
        item_output = get_output_from_source(item, document_wrapper_class)
        output.append(item_output)
    return output

def get_output_from_source(item: any, document_wrapper_class: str) -> dict:
    """
    Gets a source configuration dictionary from a source dictionary or string.

    Args:
        item (dict|str): Source configuration dictionary or string
        document_wrapper_class (str): Optional div class with which to wrap HTML.

    Returns:
        dict: Configuration dictionary with parsed HTML.
    """
    item_output = {}
    if isinstance(item, str):
        html = markdown_path(item)
    else:
        item_output = item
        html = markdown_path(item['source'])
    if document_wrapper_class:
        html = wrap_with_tag(html, document_wrapper_class)
    html_object = HTML(string=html)
    item_output['html'] = html_object
    return item_output

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
    return {
        'html': HTML(filename=decorator['template']),
        'css': CSS(filename=decorator['stylesheet'])
    }
