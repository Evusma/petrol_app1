# SQLITE operations
import psycopg
import requests
import os
import logging
import time

from psycopg_pool import ConnectionPool
from datetime import date
from streamlit_app.config import config
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DB_URL = os.environ["DB_URL"]

today = date.today()

pool = ConnectionPool(DB_URL, min_size=2, max_size=10)


# TABLE PETROL
def test_petrol():
    try:
        with pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM petrol.petrol")
            rows = cursor.fetchall()
            logger.info("total rows: %d", len(rows))
            for row in rows[-8:]:
                print(row)
    except psycopg.OperationalError as e:
        logger.error(e)


def get_data(station, max_retries=5):
    for attempt in range(max_retries):
        try:
            logger.info("API call attempt %d / %d", attempt, max_retries)
            response = requests.get(url=config.url.format(station=station))
            if response.status_code == 200:
                return response
            logger.error("Request failed with %d ", response.status_code)
        except requests.RequestException as e:
            logger.error("Request error %s", e)
        if attempt < max_retries - 1:
            delay = 2**attempt
            logger.info("Retrying in %ds...", delay)
            time.sleep(delay)
    return None


def insert_petrol(station):
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(config.create_table_petrol)
        response = get_data(station)
        if response == None:
            logger.error("No data for station %d for %s", station, today)
        else:
            response = response.json()

            id_station = response.get("id")
            brand = response.get("Brand").get("name")
            name = response.get("name")
            list_petrols = response.get("Fuels")

            for petrol in list_petrols:
                # id = 1 for the gazole
                if petrol.get("id") == 1:
                    value = petrol.get("Price").get("value")
                    value_date = petrol.get("Update").get("value")
                    cursor.execute(
                        config.insert_table_petrol,
                        (id_station, brand, name, value, value_date, today.isoformat()),
                    )
                    logger.info("inserted station %d", station)


def select_all_petrol():
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM petrol.petrol")
        rows = cursor.fetchall()
        return rows


def select_last_price_petrol():
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT max(record_date) FROM petrol.petrol")
        rows = cursor.fetchall()
        last_record_date = rows[0]
        cursor.execute(
            "SELECT * FROM petrol.petrol WHERE record_date= %s ORDER BY value ASC",
            (last_record_date,),
        )
        rows = cursor.fetchall()
        return rows


# TABLE CONTACT
def test_contact():
    try:
        with pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cv.contact")
            rows = cursor.fetchall()
            logger.info("total rows: %d", len(rows))
            for row in rows[-5:]:
                logger.info(row)
    except psycopg.OperationalError as e:
        logger.error(e)


def insert_contact(first_name, last_name, email, subject, message, linkedin):
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(config.create_table_contact)
        cursor.execute(
            config.insert_table_contact,
            (
                first_name,
                last_name,
                email,
                subject,
                message,
                linkedin,
                today.isoformat(),
                False,
            ),
        )


def select_all_contact():
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM cv.contact")
        rows = cursor.fetchall()
        return rows


def select_new_contact():
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM cv.contact WHERE NOT message_saw")
        rows = cursor.fetchall()
        return rows


def update_saw_contact(id):
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("UPDATE cv.contact SET message_saw = TRUE WHERE id = %s", (id,))


def drop_contact():
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("DROP TABLE cv.contact")
