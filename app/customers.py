from app.database import get_connection


def create_customer(first_name, last_name, email, phone, id_number):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO customers (
            first_name,
            last_name,
            email,
            phone,
            id_number
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            first_name,
            last_name,
            email,
            phone,
            id_number
        )

        cursor.execute(query, values)
        connection.commit()

        print("Customer created successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Error creating customer: {error}")

    finally:
        cursor.close()
        connection.close()