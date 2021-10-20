"""
Defines the core PDF building functions for libris.
"""
from typing import Union
import jinja2 
from weasyprint import HTML, Document
from .data_extractors import (
    get_css_data, get_decorator_data_from_styles_dict, get_default_style, get_html_data
)

def build_pdf(config: dict, be_verbose: bool) -> None:
    """
    Builds a PDF from Markdown based on a standardized configuration file.

    Args:
        config (dict): Configuration data to use for PDF generation.
        be_verbose (bool): Whether to print additional debugging information.
    """
    sources = config['sources']
    styles = config.get('styles', {})
    default_style_key = config.get('defaultStyle')
    document_wrapper_class = config.get('documentWrapperClass')
    output_file_path = config['output']
    markdown_pipe = config.get('markdownPipe', None)
    html_data = get_html_data(sources, document_wrapper_class, markdown_pipe, be_verbose)
    css_data = get_css_data(styles)
    decorator_data = get_decorator_data_from_styles_dict(styles)
    default_style = get_default_style(default_style_key, css_data)
    generate_pdf(
        html_data,
        css_data,
        decorator_data,
        default_style,
        default_style_key,
        output_file_path
    )

def generate_pdf(
        html_data: list,
        css_data: dict,
        decorator_data: dict,
        default_style: Union[list, None],
        default_style_key: Union[str, None],
        output_file_path: str
    ) -> None:
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
    count = 1
    for html_config in html_data:
        html = html_config['html']
        style_name = html_config.get('style', default_style_key)
        style = css_data.get(style_name, default_style)
        pdf = render_pdf(
            html,
            style,
            decorator_data.get(style_name, []),
            count,
            html_config.get('variables', {})
        )
        pdfs.append(pdf)
        count += len(pdf.pages)
    all_pages = gather_pages(pdfs)
    pdfs[0].copy(all_pages).write_pdf(target=output_file_path)

def render_pdf(html: str, style: list, decorator_data: list, count: int, variables: dict):
    """
    Renders a Weasyprint Document object from an HTML object and additional rendering data.

    Args:
        html (str): HTML string for the document to be rendered.
        style (list): List of styles to apply to the HTML.
        decorator_data (dict): Decorator configuration to apply.
        count (int): Current page count at the beginning of this section.
        variables (dict): Variables to be applied to decorators for the current document.
    """
    if style is None:
        pdf = html.render()
        add_decorators(pdf, decorator_data, count, variables)
        return pdf
    pdf = html.render(stylesheets=style)
    add_decorators(pdf, decorator_data, count, variables)
    return pdf

def add_decorators(pdf: Document, decorator_data: list, count: int, variables: dict):
    """
    Adds decorator data to a Weasyprint Document.

    Args:
        pdf (Document): Document object to be modified.
        decorator_data (dict): Decorator data to add to document.
        count (int): Current page count at the beginning of this section.
        variables (dict): Variables to be applied to decorators.
    """
    for page in pdf.pages:
        for decorator in decorator_data:
            final_html_string = process_decorator_template(decorator['html'], count, variables)
            html = HTML(string=final_html_string, base_url='.')
            stylesheets = get_stylesheets_for_decorator(decorator, count)
            doc = html.render(stylesheets=stylesheets)
            decorator_page = doc.pages[0]
            decorator_body = get_element(decorator_page._page_box.all_children(), 'body')
            decorator = decorator_body.copy_with_children(decorator_body.all_children())
            body = get_element(page._page_box.all_children(), 'body')
            body.children += decorator_body.all_children()
        count += 1

def get_stylesheets_for_decorator(decorator: dict, count: int) -> list:
    """
    Gets stylesheets for a decorator.

    Args:
        decorator (dict): Decorator config object.
        count (int): Current page count.

    Returns:
        list: List of CSS documents that apply to current usage of decorator.
    """
    stylesheets = [decorator['css']]
    if 'evenCss' in decorator and count % 2 == 0:
        stylesheets.append(decorator['evenCss'])
    elif 'oddCss' in decorator and count % 2 != 0:
        stylesheets.append(decorator['oddCss'])
    return stylesheets

def process_decorator_template(template: str, count: int, variables: dict) -> str:
    """
    Processes template for a decorator.

    Args:
        template (str): Base template to use.
        count (int): Current page count.
        variables (dict): Dictionary of variables to use.

    Returns:
        str: Interpolated template output.
    """
    variables['pageNumber'] = count
    template_object = jinja2.Template(template)
    return template_object.render(variables)

def get_element(boxes: any, element: str) -> any:
    """
    Gets a named element of a Weasyprint Document.

    Args:
        boxes (any): Retrieved by querying a Weasyprint Document object with
            .pages[n]._page_box.all_children()
        element (str): Name of the sub-element to find.

    Returns:
        (any): Named sub-element of the given input.
    """
    for box in boxes:
        if box.element_tag == element:
            return box
        return get_element(box.all_children(), element)


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
