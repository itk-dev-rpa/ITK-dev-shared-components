"""This module provides static functions to peform common tasks with SAP GuiGridView COM objects."""

def scroll_entire_table(grid_view, return_to_top=False) -> None:
    """This function scrolls through the entire table to load all cells.
    grid_view: A SAP GuiGridView object.
    return_to_top: Whether to return the table to the first row after scrolling.
    """
    for i in range(0, grid_view.RowCount, grid_view.VisibleRowCount):
        grid_view.FirstVisibleRow = i
    
    if return_to_top:
        grid_view.FirstVisibleRow = 0


def get_all_rows(grid_view, pre_load=True) -> tuple[tuple[str]]:
    """Get all values from a table and return them in a 2D tuple.
    grid_view: A SAP GuiGridView object.
    pre_load: Whether to first scroll through the table to load all values.
              If a row hasn't been loaded before reading, the row data will be empty.
    """
    if pre_load:
        scroll_entire_table(grid_view, True)

    columns = grid_view.ColumnOrder
    row_count = grid_view.RowCount

    output = []

    for r in range(row_count):
        row_data = []
        for c in columns:
            v = grid_view.GetCellValue(r, c)
            row_data.append(v)
        
        output.append(tuple(row_data))
    
    return tuple(output)


def get_row(grid_view, row, scroll_to_row=False) -> tuple[str]:
    """Return the data of a single row
    grid_view: A SAP GuiGridView object.
    row: The zero-based index of the row.
    scroll_to_row: Whether to scroll to the row before reading the data.
                   This ensures the data of the row has been loaded before reading.
    """
    if scroll_to_row:
        grid_view.FirstVisibleRow = row

    row_data = []
    for c in grid_view.ColumnOrder:
        v = grid_view.GetCellValue(row, c)
        row_data.append(v)
    return tuple(row_data)


def iterate_rows(grid_view) -> tuple[str]:
    """This generator yields each row of the table in order.
    This is preferable to loading all rows as this will only load a row when it's needed.
    As a side effect this function scrolls the yielded row into view, so the
    table doesn't need to be pre-loaded before calling this function.
    grid_view: A SAP GuiGridView object.
    """
    row = 0
    while row < grid_view.RowCount:
        # Only scroll when row isn't visible
        if not grid_view.FirstVisibleRow <= row <= grid_view.FirstVisibleRow + grid_view.VisibleRowCount-1:
            grid_view.FirstVisibleRow = row

        yield get_row(grid_view, row)
        row += 1


def get_column_titles(grid_view) -> tuple[str]:
    """Get the column titles of the table instead of the column ids.
    grid_view: A SAP GuiGridView object.
    """
    return tuple(grid_view.GetColumnTitles(c)[0] for c in grid_view.ColumnOrder)


def find_row_index_by_value(grid_view, column:str, value:str) -> int:
    """Find the index of the first row where the given column's value
    match the given value. Returns -1 if no row is found.
    grid_view: A SAP GuiGridView object.
    column: The name of the column whose value to check.
    value: The value to search for.
    """
    if column not in grid_view.ColumOrder:
        raise ValueError(f"Column '{column}' not in grid_view")

    for row in range(grid_view.RowCount):
        # Only scroll when row isn't visible
        if not grid_view.FirstVisibleRow <= row <= grid_view.FirstVisibleRow + grid_view.VisibleRowCount-1:
            grid_view.FirstVisibleRow = row
        
        if grid_view.GetCellValue(row, column) == value:
            return row
    
    return -1
    



if __name__=='__main__':
    import win32com.client

    SAP = win32com.client.GetObject("SAPGUI")
    app = SAP.GetScriptingEngine
    connection = app.Connections(0)
    session = connection.Sessions(0)

    table = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC1/ssubDATA_DISP_SCA:RFMCA_COV:0202/cntlRFMCA_COV_0100_CONT5/shellcont/shell")

    # print(get_row(table, 1, True))

    # scroll_entire_table(table)

    # data = get_all_rows(table)
    # print(len(data), len(data[0]))

    # for r in iterate_rows(table):
    #     print(r)
    
    # print(get_column_titles(table))
    

