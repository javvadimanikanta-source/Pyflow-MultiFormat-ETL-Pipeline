from typing import Any
from pyflow.extractors import extract_file
from pyflow.loaders import save_csv, save_parquet, load_to_database, save_json,save_zip_csv
from pyflow.logger import setup_logger
from pyflow.reports import (
    save_data_quality_report,
    save_hourly_fare_report,
    save_pickup_location_report
)
from pyflow.transformers import transform_taxi_data
from pyflow.validators import validate_required_columns, split_valid_invalid_records


def run_pipeline(config: dict[str, Any]) -> None:
    logger = setup_logger(
        config["logging"]["log_file"],
        config["logging"]["log_level"]
    )

    logger.info("PyFlow pipeline started from here:")
    df = extract_file(
    file_path=config["input"]["main_file_path"],
    file_type=config["input"]["main_file_type"]
    )
    logger.info("Input file extracted successfully")
    logger.info("Total rows extracted: %s", len(df))

    if config["processing"].get("demo_mode", False):
        limit = config["processing"]["demo_row_limit"]

        if len(df) > limit:
            df = df.head(limit)

            logger.info(
               "Demo mode enabled. Processing first %s rows only",
             limit
            )

    if "column_mapping" in config:
        df = df.rename(columns=config["column_mapping"])
        logger.info("Column standardization completed")

    validate_required_columns(
        df,
        config["validation"]["required_columns"]
    )
    logger.info("Required column validation passed")

    valid_df, invalid_df = split_valid_invalid_records(
        df=df,
        positive_columns=config["validation"]["positive_columns"],
        passenger_column="passenger_count",
        min_passenger_count=config["validation"]["min_passenger_count"],
        max_passenger_count=config["validation"]["max_passenger_count"]
    )

    logger.info("Valid rows: %s", len(valid_df))
    logger.info("Invalid rows: %s", len(invalid_df))

    if not invalid_df.empty:
        save_csv(invalid_df, config["output"]["invalid_records"])
        logger.info("Invalid records saved")

    transformed_df = transform_taxi_data(valid_df)
    logger.info("Data transformation completed")

    save_csv(transformed_df, config["output"]["processed_csv"])
    save_parquet(transformed_df, config["output"]["processed_parquet"])

    if config["output"].get("save_json", False):
     save_json(transformed_df, config["output"]["processed_json"])

    if config["output"].get("save_zip", False):
        save_zip_csv(transformed_df, config["output"]["processed_zip"])

    logger.info("Processed files saved")
    load_to_database(
    df=transformed_df,
    database_config=config["database"])

    logger.info("Data loaded into %s", config["database"]["type"])

    save_data_quality_report(
        total_rows=len(df),
        valid_rows=len(valid_df),
        invalid_rows=len(invalid_df),
        output_path=config["reports"]["data_quality_report"])

    save_hourly_fare_report(
        transformed_df,
        config["reports"]["hourly_fare_report"])

    save_pickup_location_report(
        transformed_df,
        config["reports"]["pickup_location_report"])

    logger.info("Reports generated successfully")
    logger.info("PyFlow pipeline completed successfully at this time")
    print("ETL pipeline Completed Succesfully")
    print("Total rows:", len(df))
    print("Valid rows:", len(valid_df))
    print("Invalid rows:", len(invalid_df))
    print("Clean CSV:", config["output"]["processed_csv"])
    print("Clean Parquet:", config["output"]["processed_parquet"])
    if config["output"].get("save_json", False):
        print("Clean JSON:", config["output"]["processed_json"])
    if config["output"].get("save_zip", False):
     print("Clean ZIP:", config["output"]["processed_zip"])
    print("Database type:", config["database"]["type"])
    print("Database table:", config["database"]["table_name"])

    if config["database"]["type"].lower() == "sqlite":
        print("SQLite DB:", config["database"]["sqlite_path"])

    if config["database"]["type"].lower() == "mysql":
        print("MySQL database:", config["database"]["mysql"]["database_name"])

    print("Data quality report:", config["reports"]["data_quality_report"])
    print("Hourly fare report:", config["reports"]["hourly_fare_report"])
    print("Pickup location report:", config["reports"]["pickup_location_report"])