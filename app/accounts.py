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

def view_balance(account_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT account_number, account_type, balance, status
            FROM accounts
            WHERE account_id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:
            print("Account not found.")
            return

        account_number, account_type, balance, status = account

        print("\n" + "=" * 40)
        print("          ACCOUNT BALANCE")
        print("=" * 40)
        print(f"Account Number: {account_number}")
        print(f"Account Type:   {account_type}")
        print(f"Status:         {status}")
        print(f"Balance:        R{balance:.2f}")
        print("=" * 40)

    except Exception as error:
        print(f"Unable to retrieve balance: {error}")

    finally:
        cursor.close()
        connection.close()