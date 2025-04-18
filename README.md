# ai-ticket-insights
AI-powered ticket analysis demo with Python, SQL, and GPT. Processes support data end-to-end: cleans it, summarizes issues using LLMs, and visualizes trends in a simple dashboard.

The idea is to show how AI can help make sense of support tickets by summarizing issues, tagging urgency, and pulling out trends. It's a lightweight project that combines basic data processing, LLM integration, and simple visual reporting.

It includes:
- A small ETL pipeline to clean and structure ticket data
- Integration with OpenAI to generate summaries and urgency levels
- A simple dashboard built with Streamlit (or optionally Power BI)
- Optional similarity search for related past tickets (RAG-style logic)
