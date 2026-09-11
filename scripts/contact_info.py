# calls external API and insert data into DB
import pandas as pd
import logging

from streamlit_app.config import config
from streamlit_app.services import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_data():
    contacts = database.select_all_contact()
    df = pd.DataFrame(contacts, columns=config.contact_columns)
    df["record_date"] = pd.to_datetime(df["record_date"])
    return df


def import_new_data():
    contacts = database.select_new_contact()
    df = pd.DataFrame(contacts, columns=config.contact_columns)
    df["record_date"] = pd.to_datetime(df["record_date"])
    return df


def check_new_contact():
    check_news = input("Do you want to check the new messages? (y/n)")
    while check_news:
        if check_news == "y":
            new_contacts = import_new_data()
            for row in new_contacts.itertuples():
                logger.info("Id : %d", row.id)
                logger.info(row)
                database.update_saw_contact(row.id)
                input("Press Enter to continue...")
            break
        elif check_news == "n":
            break
        else:
            check_news = input("Do you want to check the new messages? (y/n)")


def main():
    logger.info(80 * "#")
    logger.info("checking last data")

    database.test_contact()

    logger.info(80 * "#")
    contacts = import_data()
    logger.info("total all contacts: %d", len(contacts))
    logger.info(contacts)

    logger.info(80 * "#")
    new_contacts = import_new_data()
    logger.info("total new contacts: %d", len(new_contacts))

    if len(new_contacts) > 0:
        # print(new_contacts)
        check_new_contact()
    else:
        logger.info("no new contacts to check")
    # database.drop_contact()


if __name__ == "__main__":
    main()
