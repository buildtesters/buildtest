from buildtest.defaults import console
from rich.color import ANSI_COLOR_NAMES
from rich.table import Table


def print_available_colors(color_names=ANSI_COLOR_NAMES):
    """Print the available color options in a table format on background of the color option."""
    table = Table(
        "Number",
        "Color",
        header_style="bold",
        title="Available Colors",
    )
    for color, number in color_names.items():
        table.add_row(f"[black]{number}", f"[black]{color}", style="on " + color)
    console.print(table)
