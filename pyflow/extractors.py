import json
import zipfile
from pathlib import Path

import pandas as pd

from pyflow.exceptions import ExtractionError


def extract_file(file_path: str, file_type: str) -> pd.DataFrame:
    file_type = file_type.lower()

    if file_type == "csv":
        return read_csv_file(file_path)

    if file_type == "parquet":
        return read_parquet_file(file_path)

    if file_type == "json":
        return read_json_file(file_path)

    if file_type == "excel":
        return read_excel_file(file_path)

    if file_type == "zip":
        return read_zip_file(file_path)

    raise ExtractionError(f"Unsupported input file type: {file_type}")


def read_csv_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"Input file not found: {file_path}")

    try:
        return pd.read_csv(path, on_bad_lines="skip")

    except Exception as error:
        raise ExtractionError(f"Failed to read CSV file: {file_path}") from error


def read_parquet_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"Input file not found: {file_path}")

    try:
        return pd.read_parquet(path)

    except Exception as error:
        raise ExtractionError(f"Failed to read Parquet file: {file_path}") from error


def read_json_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"Input file not found: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return pd.json_normalize(data)

        return pd.json_normalize([data])

    except Exception as error:
        raise ExtractionError(f"Failed to read JSON file: {file_path}") from error


def read_excel_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"Input file not found: {file_path}")

    try:
        sheets = pd.read_excel(path, sheet_name=None)
        all_sheets = []

        for sheet_name, sheet_data in sheets.items():
            sheet_data["source_sheet"] = sheet_name
            all_sheets.append(sheet_data)

        return pd.concat(all_sheets, ignore_index=True)

    except Exception as error:
        raise ExtractionError(f"Failed to read Excel file: {file_path}") from error


def read_zip_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"Input file not found: {file_path}")

    try:
        with zipfile.ZipFile(path, "r") as zip_file:
            file_names = zip_file.namelist()

            for name in file_names:
                if name.endswith(".csv"):
                    with zip_file.open(name) as csv_file:
                        return pd.read_csv(csv_file, on_bad_lines="skip")

        raise ExtractionError("No CSV file found inside ZIP")

    except Exception as error:
        raise ExtractionError(f"Failed to read ZIP file: {file_path}") from error