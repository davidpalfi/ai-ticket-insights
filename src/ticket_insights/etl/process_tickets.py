import os
import re
from pathlib import Path

import sqlite3
import pandas as pd
import openai
from dotenv import load_dotenv

from ticket_insights.aws.s3_client import download_from_s3, upload_to_s3
from ticket_insights.core.logger import get_logger

logger = get_logger(__name__)

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

db_path = Path.cwd() / 'ticket_insights' / 'db' / 'tickets.db'
db_path.parent.mkdir(parents=True, exist_ok=True)

csv_path = Path.cwd() / 'ticket_insights' / 'output' / 'enriched_tickets.csv'
csv_path.parent.mkdir(parents=True, exist_ok=True)

download_from_s3(object_name="tickets.db", download_path=db_path)


def ensure_enriched_table(db_path: str) -> None:
    """
    (Re)create the 'enriched_tickets' table, removing any existing data.

    Args:
        db_path: Path to the SQLite database file.

    Raises:
        sqlite3.Error: On database errors.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS enriched_tickets")
    c.execute(
        """
        CREATE TABLE enriched_tickets (
            ticket_id INTEGER PRIMARY KEY,
            description TEXT,
            summary TEXT,
            urgency TEXT,
            category TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    logger.info("Recreated enriched_tickets table")
    logger.info("Ensured enriched_tickets table exists")


def get_ticket_rows(db_path: str) -> list[tuple[int, str]]:
    """
    Retrieve ticket_id and description for all open tickets in the database.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        List of tuples (ticket_id, description) for tickets with status 'Open'.

    Raises:
        sqlite3.Error: On database errors.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT ticket_id, description FROM tickets WHERE status = 'Open'")
    rows = c.fetchall()
    conn.close()
    return rows


def analyze_ticket(desc: str) -> str:
    """
    Analyze a ticket via the chat model and return the raw response.

    Args:
        desc: Ticket description text.

    Returns:
        Raw GPT output as a string.

    Raises:
        openai.error.OpenAIError: On API errors.
    """
    prompt = f"""
You're a support assistant. Analyze this ticket:

"{desc}"

Return the following fields:
Summary: A short summary of the issue in one sentence.
Urgency: One of [Low, Medium, High]
Category: A one-word category like Login, Payment, Bug, etc.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].message.content


def parse_response(gpt_output: str) -> tuple[str, str, str]:
    """
    Extract summary, urgency, and category from GPT output.

    Args:
        gpt_output: Raw output from GPT.

    Returns:
        Tuple (summary, urgency, category).
    """
    summary = urgency = category = ''
    for line in gpt_output.splitlines():
        if m := re.match(r"Summary: (.*)", line):
            summary = m.group(1)
        elif m := re.match(r"Urgency: (.*)", line):
            urgency = m.group(1)
        elif m := re.match(r"Category: (.*)", line):
            category = m.group(1)
    return summary, urgency, category


def insert_enriched(
    ticket_id: int,
    description: str,
    summary: str,
    urgency: str,
    category: str,
    db_path: str
) -> None:
    """
    Insert or replace an enriched ticket record in the database.

    Args:
        ticket_id: ID of the ticket.
        description: Original ticket description.
        summary: Generated summary.
        urgency: Generated urgency.
        category: Generated category.
        db_path: Path to the SQLite database file.

    Raises:
        sqlite3.Error: On database errors.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO enriched_tickets VALUES (?, ?, ?, ?, ?)",
        (ticket_id, description, summary, urgency, category)
    )
    conn.commit()
    conn.close()
    logger.info(f"Enriched ticket {ticket_id} saved")


def export_enriched_csv(db_path: str, csv_path: str) -> None:
    """
    Export the enriched_tickets table to a CSV file.

    Args:
        db_path: Path to the SQLite database file.
        csv_path: Path where the CSV will be written.

    Raises:
        pandas.errors.EmptyDataError: If table is empty.
    """
    df = pd.read_sql_query("SELECT * FROM enriched_tickets", sqlite3.connect(db_path))
    df.to_csv(csv_path, index=False)
    logger.info(f"Enriched tickets exported to {csv_path}")


if __name__ == "__main__":
    ensure_enriched_table(db_path)
    tickets = get_ticket_rows(db_path)
    for ticket_id, desc in tickets:
        gpt_output = analyze_ticket(desc)
        summary, urgency, category = parse_response(gpt_output)
        insert_enriched(ticket_id, desc, summary, urgency, category, db_path)

    export_enriched_csv(db_path, csv_path)

    upload_to_s3(file_path=db_path, object_name="tickets.db")
    upload_to_s3(file_path=csv_path, object_name="enriched_tickets.csv")

    logger.info("ETL process complete: database and CSV synced to S3")
