from rich.table import Table

from buildtest.defaults import console


def create_table(
    columns, data, title=None, header_style="blue", column_style=None, show_lines=False
):
    """Create a table with the given columns and data."""
    table = Table(title=title, header_style=header_style, show_lines=show_lines)
    for column in columns:
        table.add_column(column, style=column_style, overflow="fold")
    for row in data:
        table.add_row(*row)
    return table


def print_table(table, row_count=None, pager=None):
    """Print the given table, optionally showing the row count or using a pager."""
    if row_count:
        print(table.row_count)
        return
    if pager:
        with console.pager():
            console.print(table)
    else:
        console.print(table)
