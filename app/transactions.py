import uuid
from decimal import Decimal, InvalidOperation

from app.database import get_connection


def generate_reference():
    return f"TXN-{uuid.uuid4().hex[:10].upper()}"


def deposit(account_id, amount):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        amount = Decimal(str(amount))

        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return

        cursor.execute(
            """
            SELECT account_id, balance, status
            FROM accounts
            WHERE account_id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:
            print("Account not found.")
            return

        if account[2] != "ACTIVE":
            print("Transactions are only allowed on active accounts.")
            return

        reference = generate_reference()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_id = %s
            """,
            (amount, account_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions (
                account_id,
                transaction_type,
                amount,
                reference,
                description
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                account_id,
                "DEPOSIT",
                amount,
                reference,
                "Cash deposit"
            )
        )

        connection.commit()

        print("Deposit successful.")
        print(f"Amount: R{amount:.2f}")
        print(f"Reference: {reference}")

    except InvalidOperation:
        connection.rollback()
        print("Invalid deposit amount.")

    except Exception as error:
        connection.rollback()
        print(f"Deposit failed: {error}")

    finally:
        cursor.close()
        connection.close()