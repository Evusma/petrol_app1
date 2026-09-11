# calls external API and insert data into DB
import logging

from streamlit_app.config import config
from streamlit_app.services import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting database update")

    for station in config.stations:
        logger.info("Proccesing station id %d ", station)
        database.insert_petrol(station)

    logger.info("checking last data inserted:")
    database.test_petrol()


if __name__ == "__main__":
    main()
