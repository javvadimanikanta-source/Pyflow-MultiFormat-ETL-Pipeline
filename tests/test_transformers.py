import pandas as pd
from pyflow.transformers import transform_taxi_data
def test_transformer_creates_trip_duration() -> None:
    df = pd.DataFrame({
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],
        "tpep_dropoff_datetime": ["2024-01-01 10:15:00"],
        "passenger_count": [1],
        "trip_distance": [3.2],
        "fare_amount": [18.5],
        "PULocationID": [132],
        "DOLocationID": [236]
    })

    result = transform_taxi_data(df)

    assert "trip_duration_minutes" in result.columns
    assert result["trip_duration_minutes"].iloc[0] == 15