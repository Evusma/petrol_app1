# Streamlit UI
import streamlit as st


# Pages of the app
dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📈",
)
calculator = st.Page(
    "pages/calculator.py",
    title="Diesel-cost Calculator",
    icon="🧮",
)
details = st.Page(
    "pages/details.py",
    title="About the dashbboard",
    icon="⛽",
)

# Navigation menu
pg = st.navigation([dashboard, calculator, details])

pg.run()
