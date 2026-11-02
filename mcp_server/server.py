from mcp.server.fastmcp import FastMCP
from mcp_server import excel_tools, finance_tools

mcp = FastMCP("modelpilot")


@mcp.tool()
def list_sheets(file_name: str) -> list[str]:
    """List the sheet names in an Excel workbook in the data folder. Use this first."""
    return excel_tools.list_sheets(file_name)


@mcp.tool()
def sheet_info(file_name: str, sheet: str) -> dict:
    """Get the used range and column headers of a sheet. Use this to find where the data is before reading it."""
    return excel_tools.sheet_info(file_name, sheet)


@mcp.tool()
def read_range(file_name: str, sheet: str, cell_range: str) -> list[list]:
    """Read values from a cell range such as 'B2:B9'. Returns a list of rows."""
    return excel_tools.read_range(file_name, sheet, cell_range)


@mcp.tool()
def write_cell(file_name: str, sheet: str, cell: str, value: str) -> str:
    """Write one value into one cell, for example cell='B10'. Numbers are stored as numbers, anything else as text."""
    try:
        parsed = float(value)
    except ValueError:
        parsed = value
    return excel_tools.write_cell(file_name, sheet, cell, parsed)


@mcp.tool()
def calculate_growth(file_name: str, sheet: str, cell_range: str) -> dict:
    """Calculate period-over-period growth in percent for a column or row of numbers, such as revenue in 'B2:B9'. Computed in code from the workbook."""
    return finance_tools.calculate_growth(file_name, sheet, cell_range)


@mcp.tool()
def forecast_values(file_name: str, sheet: str, cell_range: str, periods: int) -> dict:
    """Forecast the next periods (1 to 12) for a range of numbers using the average growth rate. Computed in code from the workbook."""
    return finance_tools.forecast_values(file_name, sheet, cell_range, periods)


if __name__ == "__main__":
    mcp.run(transport="stdio")