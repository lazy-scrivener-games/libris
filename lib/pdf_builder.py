"""
Defines the core PDF building functions for enki.
"""

from markdown2 import markdown_path
from weasyprint import HTML, CSS

def build_pdf(config: dict) -> None:
    """
    Builds a PDF from Markdown based on a standardized configuration file.

    Args:
        config (dict): Configuration data to use for PDF generation.
    """
    sources = config['sources']
    styles = config.get('styles', {})
    default_style_key = config.get('defaultStyle')
    output_file_path = config['output']
    html_data = get_html_data(sources)
    css_data = get_css_data(styles)
    default_style = None
    if default_style_key and default_style_key in css_data:
        default_style = css_data[default_style_key]
    generate_pdf(html_data, css_data, default_style, output_file_path)

def get_html_data(sources: list) -> list:
    """
    Retrieves Weasyprint HTML objects based on a list of Markdown filenames

    Args:
        sources (list): List of source Markdown files to use

    Returns:
        list: List of dictionaries containing original configuration plus Weasyprint HTML objects.
    """
    output = []
    for item in sources:
        item_output = {}
        if isinstance(item, str):
            html = markdown_path(item)
        else:
            item_output = item
            html = markdown_path(item['source'])
        html_object = HTML(string=html)
        item_output['html'] = html_object
        output.append(item_output)
    return output

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
        else:
            output[key] = []
            for sub_value in value:
                css = CSS(filename=sub_value)
                output[key].append(css)
    return output

def generate_pdf(
        html_data: list,
        css_data: dict,
        default_style: str,
        output_file_path: str) -> None:
    """
    Creates and writes a PDF from a list of source data and config options.

    Args:
        html_data (list): List of dictionaries containing Weasyprint HTML objects and
            configuration data.
        css_data (dict): Dictionary of Weasyprint CSS objects, with keys as friendly names.
        default_style (str): Default style to use for PDF output, referencing css_data dictionary
            key.
        output_file_path (str): Path to which to write resulting PDF.
    """
    pdfs = []
    for html_config in html_data:
        html = html_config['html']
        style_name = html_config.get('style')
        style = css_data.get(style_name, default_style)
        if style is None:
            pdfs.append(html.render())
        else:
            pdfs.append(html.render(stylesheets=style))
    all_pages = gather_pages(pdfs)
    pdfs[0].copy(all_pages).write_pdf(target=output_file_path)

def gather_pages(pdfs: list) -> list:
    """
    Creates a list of pages from a list of PDFs.
    """
    output = []
    for pdf in pdfs:
        for page in pdf.pages:
            output.append(page)
    return output
