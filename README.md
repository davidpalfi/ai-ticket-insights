# ai-ticket-insights
AI-powered ticket analysis demo with Python, SQL, and GPT. Processes support data end-to-end: cleans it, summarizes issues using LLMs, and visualizes trends in a simple dashboard.

The idea is to show how AI can help make sense of support tickets by summarizing issues, tagging urgency, and pulling out trends. It's a lightweight project that combines basic data processing, LLM integration, and simple visual reporting.

It includes:
- A random ticket generator using Faker
- A small ETL pipeline to load and structure data into a SQLite database
- Integration with OpenAI to generate consistent summaries, urgency levels, and categories
- A searchable and filterable dashboard built with Streamlit (or optionally Power BI)
- (Planned) Similarity search for related past tickets using basic RAG-style logic

ai-ticket-insights/
├── data/
│   ├── generate_fake_tickets.py      #Creates fake support tickets
│   └── tickets.csv                   #Raw input data
│ 
├── db/
│   └── tickets.db                    #SQLite database (raw + enriched data)
│ 
├── etl/
│   └── process_tickets.py            #Enrichment pipeline using GPT
│ 
├── output/
│   └── enriched_tickets.csv          #Final structured output for BI
│ 
├── viz/
│   └── dashboard.py                  # Streamlit dashboard app
│ 
├── .gitignore
├── README.md
├── requirements.txt
└── .env                              #(ignored) OpenAI API key
