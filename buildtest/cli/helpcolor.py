from rich.color import ANSI_COLOR_NAMES
from rich.table import Column, Table

from buildtest.defaults import console


def print_available_colors(color_names=ANSI_COLOR_NAMES):
    """Print the available color options in a table format on background of the color option."""
    table = Table(
        Column("Number", overflow="fold"),
        Column("Color", overflow="fold"),
        header_style="bold",
        title="Available Colors",
    )
    for color, number in color_names.items():
        table.add_row(f"[black]{number}", f"[black]{color}", style="on " + color)
    console.print(table)
