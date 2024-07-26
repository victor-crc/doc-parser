import mammoth
from bs4 import BeautifulSoup


def extract_text_from_docx(docx_path: str) -> list[str]:
    """
    Extracts the text from a `.docx` file.

    Args:
        docx_path (str): The path to the `.docx` file.

    Returns:
        list[str]: A list of text passages extracted from the `.docx` file.
    """
    html = extract_html_string_from_docx(docx_path)
    return parse_text_from_html_string(html)


def extract_html_string_from_docx(docx_path: str) -> str:
    """
    Extracts the HTML string from a `.docx` file.

    Args:
        docx_path (str): The path to the `.docx` file.

    Returns:
        str: The generated HTML string.

    """
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        messages = result.messages  # Any messages, such as warnings during conversion

    if len(messages) > 0:
        for message in messages:
            print(message)

    return html


def parse_text_from_html_string(html: str) -> list[str]:
    """
    Parses an html string, that has a `.docx` as source, and extracts its text
    passages.
    Currently, it ignores tables and extracts.

    The 'docx --> html' conversion is usually done by the 'mammoth' library
    (https://github.com/mwilliamson/python-mammoth).

    Args:
        html (str): The html string to be parsed.

    Returns:
        list[str]: A list of passages extracted from the html.
    """
    soup = BeautifulSoup(html, "html.parser")
    passages = []
    for child in soup.children:
        if child.name == "table":
            passages.append("[TABELA]")
        elif child.name == "ol":
            for grandchild in child.children:
                passages.append(grandchild.text)
        else:
            passages.append(child.text)
    return passages
