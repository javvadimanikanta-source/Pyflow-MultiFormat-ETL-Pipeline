import pandas as pd

from pyflow.exceptions import TransformationError


def transform_taxi_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        transformed_df = df.copy()

        transformed_df["tpep_pickup_datetime"] = pd.to_datetime(
            transformed_df["tpep_pickup_datetime"]
        )
        transformed_df["tpep_dropoff_datetime"] = pd.to_datetime(
            transformed_df["tpep_dropoff_datetime"]
        )

        transformed_df["trip_duration_minutes"] = (
            transformed_df["tpep_dropoff_datetime"]
            - transformed_df["tpep_pickup_datetime"]
        ).dt.total_seconds() / 60

        transformed_df["pickup_hour"] = transformed_df["tpep_pickup_datetime"].dt.hour
        transformed_df["pickup_date"] = transformed_df["tpep_pickup_datetime"].dt.date

        transformed_df = transformed_df.drop_duplicates()

        return transformed_df

    except Exception as error:
        raise TransformationError("Failed to transform taxi data") from error