# vscode ➜ /workspace $ streamlit run src/streamlit_app/app.py

import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_app.config import config
from streamlit_app.services import database


@st.cache_data(ttl=600)
def import_data():
    petrol_data = database.select_all_petrol()
    df = pd.DataFrame(petrol_data, columns=config.petrol_columns)
    df["record_date"] = pd.to_datetime(df["record_date"])
    return df


def time_series_plot():
    df = import_data()

    df = df.sort_values(["name", "record_date"])

    fig = px.line(
        df,
        x="record_date",
        y="value",
        color="name",
        markers=True,
        custom_data=["value_date"],
        labels={
            "record_date": "Date",
            "value": "Price (€ / L)",
            "name": "Station",
        },
        title="Diesel Price Trends by Station",
    )

    fig.update_traces(
        hovertemplate=(
            "Station: %{fullData.name}<br>"
            "Price: %{y:.3f} € / L<br>"
            "Price updated: %{customdata[0]|%d/%m/%Y}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        hovermode="closest",
        xaxis_title="Date",
        yaxis_title="Price (€ / L)",
        legend_title="Station",
    )

    return fig


def main():
    st.title("Diesel price evolution")
    st.write("""
        Time-series dashboard to track the evolution of 
        diesel prices at selected gas stations.
    """)

    # plotly version (dynamic dahsboard)
    st.plotly_chart(time_series_plot(), width="stretch")


if __name__ == "__main__":
    main()
