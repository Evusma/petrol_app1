import streamlit as st

from datetime import date
from streamlit_app.services import database


def social_media_links():
    st.write(
        "Contact me on LinkedIn [LinkedIn](https://www.linkedin.com/in/eva-useros-marugan) "
        "or by the following contact form:"
    )


def contact_form():
    with st.form("contact_form"):
        first_name = st.text_input("First name *", max_chars=50)
        last_name = st.text_input("Last name", max_chars=50)
        email = st.text_input("Email *")
        subject = st.text_input("Subject", max_chars=100)
        message = st.text_area("Message *", max_chars=1000)
        linkedin = st.text_input("Your LinkedIn", max_chars=200)

        submitted = st.form_submit_button("Send")

        if submitted:
            if not first_name or not email or not message:
                st.error("Please fill in all required fields.")
            else:
                database.insert_contact(
                    first_name, last_name, email, subject, message, linkedin
                )
                st.success("Your message has been sent successfully! Thank you.")
                st.stop()
        st.caption(
            "Privacy: Your information is collected only to respond to your message. "
            "It is stored securely for a maximum of 12 months and is not shared with "
            "third parties, except where required by law. You may request access, "
            "correction, or deletion of your personal data."
        )


def main():
    st.title("Diesel price evolution dashboard.")
    st.write(
        """
        This is a time-series dashboard I developed to track the evolution of 
        diesel prices at gas stations near my home.
        \nAfter the significant increase in diesel prices in France since March 2026, 
        I became curious about how prices were evolving at the nearest gas stations. 
        I built this dashboard to quickly compare prices across stations, monitor 
        price trends over time, and save time when searching for the best price.
        \nThis is a personalized application tailored to my needs, helping me make 
        quicker decisions, save time, and potentially reduce my fuel expenses.
        \nThe data comes from the website 
        [datagouv](https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree)
        """
    )

    social_media_links()

    contact_form()


if __name__ == "__main__":
    main()
