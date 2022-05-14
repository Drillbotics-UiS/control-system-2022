import csv
import sqlite3


def write_db_rows(filename: str, column_names: list[str], rows: list[sqlite3.Row]):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(column_names)
        writer.writerows(rows)
