from contextlib import contextmanager
from pathlib import Path
import sqlite3
from sqlite3 import Connection
from typing import Any, Iterator
from urllib.parse import quote_plus
import zipfile
import pandas as pd
from sqlalchemy import create_engine
from pyflow.exceptions import LoadingError


def save_csv(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
def save_parquet(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)                          ##saving to required o/p formats
    df.to_parquet(path, index=False)
def save_json(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_json(path, orient="records", indent=4, date_format="iso")
def save_zip_csv(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_data = df.to_csv(index=False)

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("clean_taxi_data.csv", csv_data)

@contextmanager
def sqlite_connection(db_path: str) -> Iterator[Connection]:
    connection = sqlite3.connect(db_path)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def load_to_sqlite(
    df: pd.DataFrame,
    db_path: str,
    table_name: str,
    load_mode: str
) -> None:
    try:
        with sqlite_connection(db_path) as connection:
            df.to_sql(table_name, connection, if_exists=load_mode, index=False)

    except Exception as error:
        raise LoadingError(f"Failed to load data into SQLite table: {table_name}") from error


def load_to_mysql(
    df: pd.DataFrame,
    mysql_config: dict[str, Any],
    table_name: str,
    load_mode: str
) -> None:
    try:
        password = quote_plus(mysql_config["password"])

        connection_url = (
            f"mysql+pymysql://{mysql_config['user']}:{password}"
            f"@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database_name']}"
        )

        engine = create_engine(connection_url)
        df.to_sql(table_name, engine, if_exists=load_mode, index=False,chunksize=10000,method='multi')
        engine.dispose()

    except Exception as error:
        raise LoadingError(f"Failed to load data into MySQL table: {table_name}") from error


def load_to_database(df: pd.DataFrame, database_config: dict[str, Any]) -> None:
    database_type = database_config["type"].lower()
    table_name = database_config["table_name"]
    load_mode = database_config.get("load_mode", "replace")
    if database_type == "sqlite":
        load_to_sqlite(
            df=df,
            db_path=database_config["sqlite_path"],
            table_name=table_name,
            load_mode=load_mode
        )
        return

    if database_type == "mysql":
        load_to_mysql(
            df=df,
            mysql_config=database_config["mysql"],
            table_name=table_name,
            load_mode=load_mode
        )
        return

    raise LoadingError(f"Unsupported database type: {database_type}")