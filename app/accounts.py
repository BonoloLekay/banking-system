import random

from app.database import get_connection


def generate_account_number():
    return str(random.randint(1000000000, 9999999999))


def create_account(customer_id, account_type):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_id = %s",
            (customer_id,)
        )

        customer = cursor.fetchone()

        if not customer:
            print("Customer not found.")
            return

        if account_type not in ("SAVINGS", "CURRENT"):
            print("Invalid account type.")
            return

        account_number = generate_account_number()

        query = """
        INSERT INTO accounts (
            customer_id,
            account_number,
            account_type
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                customer_id,
                account_number,
                account_type
            )
        )

        connection.commit()

        print("Account created successfully.")
        print(f"Account number: {account_number}")

    except Exception as error:
        connection.rollback()
        print(f"Error creating account: {error}")

    finally:
        cursor.close()
        connection.close()