from app.database import get_connection


def test_test_database_connection():
    connection = get_connection(testing=True)

    assert connection.is_connected()

    connection.close()