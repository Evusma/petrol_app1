import streamlit as st
import pandas as pd

from streamlit_app.config import config
from streamlit_app.services import database


def import_data():
    last_price = database.select_last_price_petrol()
    df = pd.DataFrame(last_price, columns=config.petrol_columns)
    return df


def fuel_calculator(df):
    st.subheader("🛢️ Fuel cost calculator")

    stations = sorted(df["name"].unique())

    with st.form("fuel_calculator"):
        station = st.selectbox(
            "Choose a station",
            stations,
        )

        liters = st.number_input(
            "How many liters?",
            min_value=1.0,
            step=1.0,
            value=50.0,
        )

        submitted = st.form_submit_button("Calculate")

    if submitted:
        # Price at selected station
        selected_row = df[df["name"] == station].iloc[0]
        selected_price = selected_row["value"]

        # Cheapest station
        cheapest_row = df.loc[df["value"].idxmin()]
        cheapest_station = cheapest_row["name"]
        cheapest_price = cheapest_row["value"]

        # Costs
        selected_cost = liters * selected_price
        cheapest_cost = liters * cheapest_price
        saving = selected_cost - cheapest_cost

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Your cost",
                f"{selected_cost:.2f} €",
                f"{selected_price:.3f} €/L",
            )

        with col2:
            st.metric(
                "Cheapest cost",
                f"{cheapest_cost:.2f} €",
                f"{cheapest_price:.3f} €/L",
            )

        st.info(
            f"💡 The cheapest station is **{cheapest_station}** "
            f"at **{cheapest_price:.3f} €/L**."
        )

        if saving > 0:
            st.success(
                f"You could save **{saving:.2f} €** by choosing {cheapest_station}."
            )
        else:
            st.success("🎉 You already chose the cheapest station!")


def main():
    df = import_data()
    fuel_calculator(df)


if __name__ == "__main__":
    main()
