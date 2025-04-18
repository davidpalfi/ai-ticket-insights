import sqlite3
import openai
import os
import re
import pandas as pd
from dotenv import load_dotenv

#Load OpenAI key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Ensure enriched_tickets table exists
def ensure_enriched_table(db_path="db/tickets.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS enriched_tickets (
            ticket_id INTEGER PRIMARY KEY,
            description TEXT,
            summary TEXT,
            urgency TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

#Read open tickets from DB
def get_ticket_rows(db_path="db/tickets.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT ticket_id, description FROM tickets
        WHERE status = 'Open'
        ORDER BY created_at ASC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

#Send ticket description to GPT
def analyze_ticket(desc):
    prompt = f"""
You're a support assistant. Analyze this ticket:

"{desc}"

Return:
Summary: ...
Urgency: ...
Category: ...
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].message.content

#Extract structured info from GPT response
def parse_response(text):
    summary = re.search(r"Summary:\s*(.+)", text, re.IGNORECASE)
    urgency = re.search(r"Urgency:\s*(.+)", text, re.IGNORECASE)
    category = re.search(r"Category:\s*(.+)", text, re.IGNORECASE)

    return (
        summary.group(1).strip() if summary else "",
        urgency.group(1).strip() if urgency else "",
        category.group(1).strip() if category else ""
    )

#Insert into enriched_tickets table
def insert_enriched(ticket_id, desc, summary, urgency, category, db_path="db/tickets.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO enriched_tickets
        (ticket_id, description, summary, urgency, category)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, desc, summary, urgency, category))
    conn.commit()
    conn.close()

#Export final enriched table to CSV
def export_enriched_csv(db_path="db/tickets.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM enriched_tickets", conn)
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/enriched_tickets.csv", index=False)
    conn.close()
    print(f"\nSaved {len(df)} enriched tickets to output/enriched_tickets.csv")

#Main script
if __name__ == "__main__":
    ensure_enriched_table()
    tickets = get_ticket_rows()
    
    for ticket_id, desc in tickets:
        print(f"\n--- Ticket {ticket_id} ---")
        gpt_output = analyze_ticket(desc)
        print(gpt_output)

        summary, urgency, category = parse_response(gpt_output)
        insert_enriched(ticket_id, desc, summary, urgency, category)

    export_enriched_csv()
