from pathlib import Path
import sqlite3

import pandas as pd


DB_PATH = Path("data/raw/risk_monitor_dataset.sqlite")
print(f"Database path: {DB_PATH}")

def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def get_tables(connection: sqlite3.Connection) -> list[str]:
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
    """
    rows = connection.execute(query).fetchall()
    return [row[0] for row in rows]


def print_table_overview(connection: sqlite3.Connection, table_name: str) -> None:
    quoted_table_name = quote_identifier(table_name)

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {quoted_table_name};"
    ).fetchone()[0]

    schema = pd.read_sql_query(f"PRAGMA table_info({quoted_table_name});", connection)
    first_rows = pd.read_sql_query(
        f"SELECT * FROM {quoted_table_name} LIMIT 5;",
        connection,
    )

    print("=" * 80)
    print(f"Table: {table_name}")
    print(f"Number of rows: {row_count}")

    print("\nSchema:")
    print(schema[["name", "type"]].to_string(index=False))

    print("\nFirst 5 rows:")
    print(first_rows.to_string(index=False))
    print()


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as connection:
        tables = get_tables(connection)

        print(f"Database: {DB_PATH}")
        print(f"Tables found: {len(tables)}")

        if not tables:
            print("No tables found.")
            return

        print("\nAll tables:")
        for table_name in tables:
            print(f"- {table_name}")

        print()
        for table_name in tables:
            print_table_overview(connection, table_name)


if __name__ == "__main__":
    main()
