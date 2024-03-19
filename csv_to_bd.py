import csv
import sqlite3

def create_table(cursor, headers, sample_row):
    columns = []
    for header, value in zip(headers, sample_row):
        data_type = 'TEXT'
        if value.isnumeric():
            data_type = 'INTEGER'
        elif value.replace('.', '', 1).isnumeric():
            data_type = 'REAL'
        columns.append(f"{header} {data_type}")
    cursor.execute(f"CREATE TABLE data ({', '.join(columns)})")

def insert_data(cursor, row):
    placeholders = ', '.join(['?'] * len(row))
    cursor.execute(f"INSERT INTO data VALUES ({placeholders})", row)

def csv_to_sqlite(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        headers = list([i.lower().replace(" ", "_") for i in headers])
        print(headers)
        sample_row = next(csv_reader)
        create_table(cursor, headers, sample_row)
        insert_data(cursor, sample_row)

        for row in csv_reader:
            insert_data(cursor, row)

    conn.commit()
    conn.close()

csv_to_sqlite('car_details_v4.csv', 'main.db')
