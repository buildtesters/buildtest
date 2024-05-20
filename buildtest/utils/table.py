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


def print_terse_format(tdata, headers, color=None, display_header=False, pager=None):
    """This method will print the output of ``buildtest buildspec find`` in terse format.

    Args:
        tdata (list): Table data to print in terse format
        headers (list): List of headers to print in terse format
    Returns:

    """

    # print terse output
    if not display_header:
        console.print("|".join(headers), style=color)

    if not tdata:
        return

    for row in tdata:
        if not isinstance(row, list):
            continue

        # if any entry contains None type we convert to empty string
        row = ["" if item is None else item for item in row]
        join_string = "|".join(row)

        if pager:
            with console.pager():
                console.print(f"[{color}]{join_string}")
        else:
            console.print(f"[{color}]{join_string}")
