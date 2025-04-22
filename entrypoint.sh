#!/bin/bash
set -e

#Generate synthetic support tickets using Faker
python3 data/generate_fake_tickets.py

#Initialize the SQLite database with raw ticket data
python3 db/init_db.py

#Enrich tickets using OpenAI's API (requires OPENAI_API_KEY)
python3 etl/process_tickets.py

#Launch the Streamlit dashboard
exec streamlit run viz/dashboard.py
