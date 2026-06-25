import pandas as pd
from pyflow.loaders import save_csv
def test_save_csv_creates_file(tmp_path) -> None:
    df = pd.DataFrame({
        "name": ["modi"],
        "marks": [99]
    })

    output_file = tmp_path / "output.csv"

    save_csv(df, str(output_file))

    assert output_file.exists()