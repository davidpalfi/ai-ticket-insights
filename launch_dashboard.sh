#!/usr/bin/env bash
set -e

#Run from repo root so imports resolve correctly
cd "$(dirname "$0")"

#Make our project root importable by Streamlit
export PYTHONPATH="$(pwd)"
streamlit run viz/dashboard.py
