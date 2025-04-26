#!/usr/bin/env bash
set -e

#Ensure we’re in the repo root
cd "$(dirname "$0")/.."

#Add src/ to PYTHONPATH so ticket_insights package is importable
export PYTHONPATH="$(pwd)/src"
streamlit run src/ticket_insights/viz/dashboard.py
