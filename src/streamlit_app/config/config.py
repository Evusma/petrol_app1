stations = (
    94400003,
    94400005,
    94400004,
    94140004,
    94110003,
)
url = "https://api.prix-carburants.2aaz.fr/station/{station}"

petrol_columns = [
    "id",
    "id_station",
    "brand",
    "name",
    "value",
    "value_date",
    "record_date",
]

create_table_petrol = """
    CREATE TABLE IF NOT EXISTS petrol.petrol (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        id_station INTEGER NOT NULL,
        brand TEXT,
        name TEXT,
        value REAL,
        value_date TEXT,
        record_date DATE,
        UNIQUE (id_station, record_date)
    )
"""

insert_table_petrol = """
    INSERT INTO petrol.petrol (
        id_station,
        brand,
        name,
        value,
        value_date,
        record_date
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
"""

contact_columns = [
    "id",
    "first_name",
    "last_name",
    "email",
    "subject",
    "message",
    "linkedin",
    "record_date",
    "message_saw",
]

create_table_contact = """
    CREATE TABLE IF NOT EXISTS cv.contact (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT,
        email TEXT NOT NULL,
        subject TEXT,
        message TEXT NOT NULL,
        linkedin TEXT,
        record_date DATE,
        message_saw BOOLEAN NOT NULL DEFAULT FALSE,
        UNIQUE (first_name, email, message, record_date)
    )
"""

insert_table_contact = """
    INSERT INTO cv.contact (
        first_name,
        last_name,
        email,
        subject,
        message,
        linkedin,
        record_date,
        message_saw
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
"""
