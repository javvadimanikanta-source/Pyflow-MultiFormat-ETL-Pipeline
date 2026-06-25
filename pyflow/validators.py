import pandas as pd

from pyflow.exceptions import ValidationError


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str]
) -> None:
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValidationError(f"Missing required columns: {missing_columns}")
def split_valid_invalid_records(
    df: pd.DataFrame,
    positive_columns: list[str],
    passenger_column: str,
    min_passenger_count: int,
    max_passenger_count: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = pd.Series(True, index=df.index)

    for column in positive_columns:
        valid_mask = valid_mask & (df[column] > 0)

    valid_mask = valid_mask & (
        df[passenger_column].between(min_passenger_count, max_passenger_count)
    )

    valid_df = df[valid_mask].copy()
    invalid_df = df[~valid_mask].copy()

    return valid_df, invalid_df