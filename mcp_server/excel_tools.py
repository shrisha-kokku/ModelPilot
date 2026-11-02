from pathlib import Path
from openpyxl import load_workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _resolve(file_name: str) -> Path:
    """Only files inside the data folder are allowed."""
    path = (DATA_DIR / file_name).resolve()
    if DATA_DIR.resolve() not in path.parents:
        raise ValueError("Access denied: file must be inside the data folder.")
    if not path.exists():
        raise ValueError(f"File not found: {file_name}. Available: {[p.name for p in DATA_DIR.glob('*.xlsx')]}")
    return path


def _get_sheet(wb, sheet: str):
    if sheet not in wb.sheetnames:
        raise ValueError(f"Sheet '{sheet}' not found. Available: {wb.sheetnames}")
    return wb[sheet]


def list_sheets(file_name: str) -> list[str]:
    """List the sheet names in a workbook."""
    return load_workbook(_resolve(file_name)).sheetnames


def sheet_info(file_name: str, sheet: str) -> dict:
    """Return the used range and the header row, so the agent knows where the data is."""
    ws = _get_sheet(load_workbook(_resolve(file_name), data_only=True), sheet)
    return {"dimensions": ws.dimensions, "headers": [c.value for c in ws[1]]}


def read_range(file_name: str, sheet: str, cell_range: str) -> list[list]:
    """Read values from a cell or range, for example 'B2:B9'."""
    ws = _get_sheet(load_workbook(_resolve(file_name), data_only=True), sheet)
    cells = ws[cell_range]
    if not isinstance(cells, tuple):
        return [[cells.value]]
    return [[c.value for c in row] for row in cells]


def write_cell(file_name: str, sheet: str, cell: str, value: float | str) -> str:
    """Write one value into one cell."""
    path = _resolve(file_name)
    wb = load_workbook(path)
    _get_sheet(wb, sheet)[cell] = value
    wb.save(path)
    return f"Wrote {value} to {sheet}!{cell}"