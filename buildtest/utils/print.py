from rich.syntax import Syntax

from buildtest.defaults import console
from buildtest.utils.file import read_file


def print_file_content(file_path, title, lexer, theme, show_last_lines=None):
    """This method will print the content of a file using Rich Syntax.
    Args:
        file_path (str): Specify file to print the content of.
        title (str): The title to use when printing the content.
        lexer (str): The lexer to use when printing the content.
        theme (str): The theme to use when printing the content.
        show_last_lines (int): Show last N lines of file content. If set to None, will print entire file content.
    """

    content = read_file(file_path)
    console.rule(title)

    trimmed_content = None

    if show_last_lines:
        trimmed_content = content.split("\n")[-show_last_lines:]
        trimmed_content = "\n".join(trimmed_content)

    # if trimmed content is set, we will print a reduced content output otherwise will print entire file
    content = trimmed_content or content

    syntax = Syntax(content, lexer, theme=theme)
    console.print(syntax)
    console.rule()


def print_content(content, title, lexer, theme, show_last_lines=None):
    """This method will print the content using Rich Syntax.

    Args:
        content (str): Specify file to print the content of.
        title (str): The title to use when printing the content.
        lexer (str): The lexer to use when printing the content.
        theme (str): The theme to use when printing the content.
        show_last_lines (int): Show last N lines of file content. If set to None, will print entire file content.
    """

    console.rule(title)

    trimmed_content = None

    if show_last_lines:
        trimmed_content = content.split("\n")[-show_last_lines:]
        trimmed_content = "\n".join(trimmed_content)

    # if trimmed content is set, we will print a reduced content output otherwise will print entire file
    content = trimmed_content or content

    syntax = Syntax(content, lexer, theme=theme)
    console.print(syntax)
    console.rule()
