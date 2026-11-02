from pathlib import Path
from openpyxl import Workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

ROWS = [
    ("Q1 2024", 1200, 180), ("Q2 2024", 1260, 195),
    ("Q3 2024", 1350, 210), ("Q4 2024", 1440, 230),
    ("Q1 2025", 1500, 240), ("Q2 2025", 1620, 265),
    ("Q3 2025", 1710, 280), ("Q4 2025", 1830, 310),
]


def create_sample() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Income Statement"
    ws.append(["Quarter", "Revenue", "Net Income", "Revenue Growth %"])
    for row in ROWS:
        ws.append(row)
    wb.save(DATA_DIR / "sample_model.xlsx")
    print("Created data/sample_model.xlsx")


if __name__ == "__main__":
    create_sample()