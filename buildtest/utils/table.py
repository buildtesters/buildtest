from rich.table import Table

from buildtest.defaults import console


def create_table(
    columns, data, title=None, header_style="blue", column_style=None, show_lines=False
):
    """Create a table object with the given columns and data. This function is a wrapper around rich.Table
    and it can be used to alter table settings. The return value is a rich.Table object.

    Args:
        columns (list): List of column names
        data (list): List of rows, where each row is a list of values
        title (str): Title of the table
        header_style (str): Style of the header
        column_style (str): Style of the columns
        show_lines (bool): Whether to show lines in the table

    """
    table = Table(title=title, header_style=header_style, show_lines=show_lines)
    for column in columns:
        table.add_column(column, style=column_style, overflow="fold")
    for row in data:
        table.add_row(*row)
    return table


def print_table(table, row_count=None, pager=None):
    """Print the given table, optionally showing the row count or using a pager.

    Args:
        table (Table): Table to print
        row_count (bool): Whether to show the row count
        pager (bool): Whether to use a pager
    """
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
        color (str): Specify color to use when printing output
        display_header (bool): Display header when printing output
        pager (bool): Use pager when printing output

    """

    def print_data(tdata):
        """Print the data in terse format.

        Args:
            data (list): Data to print in terse format
        """
        # print terse output
        if not display_header:
            console.print("|".join(headers), style=color)

        for row in tdata:
            if not isinstance(row, list):
                continue

            # if any entry contains None type we convert to empty string
            row = ["" if item is None else item for item in row]
            join_string = "|".join(row)

            console.print(f"[{color}]{join_string}")

    if not tdata:
        return

    if pager:
        with console.pager():
            print_data(tdata)
    else:
        print_data(tdata)
