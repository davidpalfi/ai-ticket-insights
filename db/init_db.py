import sqlite3
import csv

def init_db(db_path="db/tickets.db", csv_path="data/tickets.csv"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tickets")
    c.execute("""
        CREATE TABLE tickets (
            ticket_id INTEGER PRIMARY KEY,
            created_at TEXT,
            subject TEXT,
            description TEXT,
            status TEXT,
            product TEXT
        )
    """)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [
            (
                int(row['ticket_id']),
                row['created_at'],
                row['subject'],
                row['description'],
                row['status'],
                row['product']
            )
            for row in reader
        ]

    c.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)", rows)
    conn.commit()
    conn.close()
    print(f"Loaded {len(rows)} tickets into {db_path}")

if __name__ == "__main__":
    init_db()
