"""
Defines the core PDF building functions for enki.
"""

from lib.data_extractors import (
    get_css_data, get_decorator_data_from_styles_dict, get_default_style, get_html_data
)


def build_pdf(config: dict) -> None:
    """
    Builds a PDF from Markdown based on a standardized configuration file.

    Args:
        config (dict): Configuration data to use for PDF generation.
    """
    sources = config['sources']
    styles = config.get('styles', {})
    default_style_key = config.get('defaultStyle')
    document_wrapper_class = config.get('documentWrapperClass')
    output_file_path = config['output']
    html_data = get_html_data(sources, document_wrapper_class)
    css_data = get_css_data(styles)
    decorator_data = get_decorator_data_from_styles_dict(styles)
    default_style = get_default_style(default_style_key, css_data)
    generate_pdf(html_data, css_data, decorator_data, default_style, output_file_path)

def generate_pdf(
        html_data: list,
        css_data: dict,
        decorator_data: dict,
        default_style: str,
        output_file_path: str) -> None:
    """
    Creates and writes a PDF from a list of source data and config options.

    Args:
        html_data (list): List of dictionaries containing Weasyprint HTML objects and
            configuration data.
        css_data (dict): Dictionary of Weasyprint CSS objects, with keys as friendly names.
        decorator_data (dict): Dictionary of data about applicable decorators for each style
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

    Args:
        pdfs (list): List of PDFs to collate.

    Returns:
        list: List of pages from all passed PDFs.
    """
    output = []
    for pdf in pdfs:
        for page in pdf.pages:
            output.append(page)
    return output
