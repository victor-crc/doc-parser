from bs4 import BeautifulSoup


def parse_html_from_docx(html: str) -> list[str]:
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
