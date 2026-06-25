import pandas as pd
import pytest
from pyflow.exceptions import ValidationError
from pyflow.validators import validate_required_columns
def test_required_column_validation_passes() -> None:
    df = pd.DataFrame({
        "passenger_count": [1],
        "fare_amount": [20.0]
    })

    validate_required_columns(df, ["passenger_count", "fare_amount"])
def test_required_column_validation_fails() -> None:
    df = pd.DataFrame({
        "passenger_count": [1]
    })

    with pytest.raises(ValidationError):
        validate_required_columns(df, ["passenger_count", "fare_amount"])