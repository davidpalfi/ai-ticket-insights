import sqlite3
import csv
from dotenv import load_dotenv
from pathlib import Path

from ticket_insights.aws.s3_client import download_from_s3, upload_to_s3
from ticket_insights.core.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


def init_db(db_path: str, csv_path: str) -> None:
    """
    Initialize the SQLite database using ticket data from a CSV file.

    Args:
        db_path: Path to the SQLite database file to create or overwrite.
        csv_path: Path to the CSV file containing tickets.

    Raises:
        sqlite3.Error: On database errors.
        IOError: If reading the CSV fails.
    """
    logger.info(f"Initializing database '{db_path}' from CSV '{csv_path}'")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tickets")
    c.execute(
        """
        CREATE TABLE tickets (
            ticket_id INTEGER PRIMARY KEY,
            created_at TEXT,
            subject TEXT,
            description TEXT,
            status TEXT,
            product TEXT
        )
        """
    )

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(
            int(r["ticket_id"]),
            r["created_at"],
            r["subject"],
            r["description"],
            r["status"],
            r["product"]
        ) for r in reader]

    c.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)", rows)
    conn.commit()
    conn.close()
    logger.info(f"Loaded {len(rows)} tickets into '{db_path}'")


if __name__ == "__main__":
    db_dir = Path.cwd() / 'ticket_insights' / 'db'
    db_dir.mkdir(parents=True, exist_ok=True)

    csv_path = db_dir / 'tickets.csv'
    db_path  = db_dir / 'tickets.db'

    download_from_s3(object_name='tickets.csv', download_path=csv_path)
    init_db(db_path=db_path, csv_path=csv_path)
    upload_to_s3(file_path=db_path, object_name='tickets.db')

    csv_path.unlink(missing_ok=True)
