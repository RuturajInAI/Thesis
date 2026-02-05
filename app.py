import streamlit as st
from components.wizard import run_wizard

st.set_page_config(page_title="Weld HMI", layout="wide")

run_wizard()
