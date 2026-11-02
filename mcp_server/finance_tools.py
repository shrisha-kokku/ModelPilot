from mcp_server.excel_tools import read_range


def _numbers(file_name: str, sheet: str, cell_range: str) -> list[float]:
    rows = read_range(file_name, sheet, cell_range)
    values = [v for row in rows for v in row]
    if any(not isinstance(v, (int, float)) for v in values):
        raise ValueError(f"Range {cell_range} must contain only numbers. Found: {values}")
    return [float(v) for v in values]


def _growth_rates(values: list[float]) -> list[float]:
    if len(values) < 2:
        raise ValueError("Need at least 2 values to calculate growth.")
    rates = []
    for previous, current in zip(values, values[1:]):
        if previous == 0:
            raise ValueError("Cannot calculate growth from a value of 0.")
        rates.append((current - previous) / previous * 100)
    return rates


def calculate_growth(file_name: str, sheet: str, cell_range: str) -> dict:
    """Period-over-period growth in percent for a column or row of numbers."""
    values = _numbers(file_name, sheet, cell_range)
    rates = _growth_rates(values)
    return {
        "source": f"{sheet}!{cell_range}",
        "values": values,
        "growth_percent": [round(r, 2) for r in rates],
        "average_growth_percent": round(sum(rates) / len(rates), 2),
    }


def forecast_values(file_name: str, sheet: str, cell_range: str, periods: int) -> dict:
    """Forecast the next periods by applying the average growth rate."""
    if not 1 <= periods <= 12:
        raise ValueError("periods must be between 1 and 12.")
    values = _numbers(file_name, sheet, cell_range)
    rates = _growth_rates(values)
    average = sum(rates) / len(rates)
    forecast, last = [], values[-1]
    for _ in range(periods):
        last = last * (1 + average / 100)
        forecast.append(round(last, 2))
    return {
        "source": f"{sheet}!{cell_range}",
        "method": "average growth rate",
        "average_growth_percent": round(average, 2),
        "forecast": forecast,
    }