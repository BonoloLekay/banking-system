import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection(testing=False):
    database_name = (
        os.getenv("TEST_DB_NAME")
        if testing
        else os.getenv("DB_NAME")
    )

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=database_name
    )

    return connection