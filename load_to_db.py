import os

import duckdb

from timers import timer


def _list_files_in_dir(data_dir: str) -> list:
    return [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if os.path.isfile(os.path.join(data_dir, f)) and f.endswith(".csv")
    ]


def _load_file_as_table(file_path: str) -> None:
    table_name = os.path.splitext(os.path.basename(file_path))[0]
    duckdb.sql(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}');")


@timer
def load_files_as_tables(data_dir: str) -> None:
    for f in _list_files_in_dir(data_dir):
        _load_file_as_table(f)
