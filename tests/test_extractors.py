from pyflow.extractors import extract_file
def test_csv_extractor_reads_file() -> None:
    df = extract_file("data/raw/sample_taxi.csv", "csv")

    assert len(df) > 0
    assert "trip_distance" in df.columns