import streamlit as st
import pandas as pd
from pathlib import Path
from aws.s3_utils import download_from_s3

csv_path = Path.cwd() / 'viz' / 'enriched_tickets.csv'
csv_path.parent.mkdir(parents=True, exist_ok=True)

download_from_s3(object_name='enriched_tickets.csv', download_path=csv_path)
df = pd.read_csv(csv_path)
csv_path.unlink(missing_ok=True)

st.set_page_config(page_title="AI Ticket Insights", layout="wide")

st.title("AI Ticket Insights Dashboard")

# --------------------------------------------------------------------------------
# Sidebar filters
# --------------------------------------------------------------------------------
st.sidebar.header("Filter tickets")

urgency_filter = st.sidebar.multiselect(
    "Urgency",
    options=df["urgency"].unique(),
    default=df["urgency"].unique(),
)

category_filter = st.sidebar.multiselect(
    "Category",
    options=df["category"].unique(),
    default=df["category"].unique(),
)

filtered_df = df[
    (df["urgency"].isin(urgency_filter)) &
    (df["category"].isin(category_filter))
]

# --------------------------------------------------------------------------------
# KPIs
# --------------------------------------------------------------------------------
st.markdown("### Ticket Summary")
col1, col2 = st.columns(2)
col1.metric("Total Tickets Open", len(filtered_df))
col2.metric("Unique Categories", filtered_df["category"].nunique())

# --------------------------------------------------------------------------------
# Charts
# --------------------------------------------------------------------------------
st.markdown("### Open Tickets by Category")
st.bar_chart(filtered_df["category"].value_counts())

st.markdown("### Urgency Distribution")
st.bar_chart(filtered_df["urgency"].value_counts())

# --------------------------------------------------------------------------------
# Data table
# --------------------------------------------------------------------------------
st.markdown("### Ticket Details")
st.dataframe(filtered_df[["ticket_id", "summary", "urgency", "category"]])
