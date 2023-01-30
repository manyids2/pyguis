"""
Read, write with sqlite3 databases and pandas DataFrames.
"""
from typing import Union, List
from pathlib import Path
import sqlite3
import pandas as pd


def save_db(
    df: pd.DataFrame,
    db_path: Union[Path, str],
    table: str,
    if_exists: str = "replace",
    index: bool = False,
    verbose: bool = False,
) -> None:
    """Save DataFrame to sqlite3 db as specified table.
    NOTE: default behaviour is to replace the table if it exists."""
    conn = sqlite3.connect(str(db_path))

    if len(df.columns) == 0:
        print(f"Cannot save empty df ->\n{df}")
        return

    df.to_sql(table, conn, if_exists=if_exists, index=index)
    if verbose:
        print(df)
        print(df.columns)
        print(f"Saved to => {table} => {db_path}")


def load_db(
    db_path: Union[Path, str], table: str, verbose: bool = False
) -> pd.DataFrame:
    """Read sqlite3 db, return all rows from specified table."""
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query(f"SELECT * from '{table}'", conn)
    if verbose:
        print(df)
        print(df.columns)
    return df


def get_tables(db_path: Union[Path, str], verbose: bool = False) -> List[str]:
    """Read sqlite3 db, return table names."""
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query(f'SELECT name FROM sqlite_master WHERE type = "table"', conn)
    if verbose:
        print(df)
    return list(df.name)


def gen_csv(csv_path: Path, url: str) -> None:
    rows = []
    for color in ["red", "green", "blue"]:
        row = {
            "color": color,
            "image": f"{url}/{color}.png",
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="./data/images.csv", type=Path)
    parser.add_argument("--url", default="http://localhost:5555", type=str)
    args = parser.parse_args()

    gen_csv(args.csv_path, args.url)
