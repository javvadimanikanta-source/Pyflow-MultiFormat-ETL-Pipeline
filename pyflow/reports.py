from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd


def save_data_quality_report(
    total_rows: int,
    valid_rows: int,
    invalid_rows: int,
    output_path: str
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report = pd.DataFrame([
        {
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "invalid_rows": invalid_rows,
            "rejection_rate": round(invalid_rows / total_rows, 3)
        }
    ])

    report.to_csv(path, index=False)


def save_hourly_fare_report(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    hourly_fares = defaultdict(list)

    for _, row in df.iterrows():
        hourly_fares[int(row["pickup_hour"])].append(float(row["fare_amount"]))

    rows = []

    for hour, fares in hourly_fares.items():
        rows.append({
            "pickup_hour": hour,
            "trip_count": len(fares),
            "average_fare": round(sum(fares) / len(fares), 2)
        })

    report = pd.DataFrame(rows).sort_values("pickup_hour")
    report.to_csv(path, index=False)


def save_pickup_location_report(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    pickup_counts = Counter(df["PULocationID"])

    report = pd.DataFrame([
        {
            "PULocationID": location_id,
            "trip_count": count
        }
        for location_id, count in pickup_counts.items()
    ])

    report = report.sort_values("trip_count", ascending=False)
    report.to_csv(path, index=False)