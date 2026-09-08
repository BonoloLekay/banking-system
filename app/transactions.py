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

def withdraw(account_id, amount):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        amount = Decimal(str(amount))

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return

        cursor.execute(
            """
            SELECT balance, status
            FROM accounts
            WHERE account_id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:
            print("Account not found.")
            return

        balance = account[0]
        status = account[1]

        if status != "ACTIVE":
            print("Transactions are only allowed on active accounts.")
            return

        if amount > balance:
            print("Insufficient funds.")
            return

        reference = generate_reference()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
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
                "WITHDRAWAL",
                amount,
                reference,
                "Cash withdrawal"
            )
        )

        connection.commit()

        print("Withdrawal successful.")
        print(f"Amount: R{amount:.2f}")
        print(f"Reference: {reference}")

    except InvalidOperation:
        connection.rollback()
        print("Invalid withdrawal amount.")

    except Exception as error:
        connection.rollback()
        print(f"Withdrawal failed: {error}")

    finally:
        cursor.close()
        connection.close()

def transfer(from_account_id, to_account_id, amount):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        amount = Decimal(str(amount))

        if amount <= 0:
            print("Transfer amount must be greater than zero.")
            return

        if from_account_id == to_account_id:
            print("You cannot transfer money to the same account.")
            return

        cursor.execute(
            """
            SELECT balance, status
            FROM accounts
            WHERE account_id = %s
            """,
            (from_account_id,)
        )

        sender = cursor.fetchone()

        if not sender:
            print("Sender account not found.")
            return

        sender_balance = sender[0]
        sender_status = sender[1]

        if sender_status != "ACTIVE":
            print("Sender account is not active.")
            return

        cursor.execute(
            """
            SELECT status
            FROM accounts
            WHERE account_id = %s
            """,
            (to_account_id,)
        )

        receiver = cursor.fetchone()

        if not receiver:
            print("Receiver account not found.")
            return

        if receiver[0] != "ACTIVE":
            print("Receiver account is not active.")
            return

        if amount > sender_balance:
            print("Insufficient funds.")
            return

        reference = generate_reference()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_id = %s
            """,
            (amount, from_account_id)
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_id = %s
            """,
            (amount, to_account_id)
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
                from_account_id,
                "TRANSFER_OUT",
                amount,
                f"{reference}-OUT",
                f"Transfer to account {to_account_id}"
            )
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
                to_account_id,
                "TRANSFER_IN",
                amount,
                f"{reference}-IN",
                f"Transfer from account {from_account_id}"
            )
        )

        connection.commit()

        print("Transfer successful.")
        print(f"Amount: R{amount:.2f}")
        print(f"Reference: {reference}")

    except InvalidOperation:
        connection.rollback()
        print("Invalid transfer amount.")

    except Exception as error:
        connection.rollback()
        print(f"Transfer failed: {error}")

    finally:
        cursor.close()
        connection.close()

def view_transaction_history(account_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT account_number
            FROM accounts
            WHERE account_id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:
            print("Account not found.")
            return

        cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                reference,
                description,
                created_at
            FROM transactions
            WHERE account_id = %s
            ORDER BY created_at DESC
            """,
            (account_id,)
        )

        transactions = cursor.fetchall()

        print("\n" + "=" * 70)
        print(f"TRANSACTION HISTORY - {account[0]}")
        print("=" * 70)

        if not transactions:
            print("No transactions found.")
            return

        for transaction in transactions:
            transaction_type = transaction[0]
            amount = transaction[1]
            reference = transaction[2]
            description = transaction[3]
            created_at = transaction[4]

            print(f"Type:        {transaction_type}")
            print(f"Amount:      R{amount:.2f}")
            print(f"Reference:   {reference}")
            print(f"Description: {description}")
            print(f"Date:        {created_at}")
            print("-" * 70)

    except Exception as error:
        print(f"Unable to retrieve transaction history: {error}")

    finally:
        cursor.close()
        connection.close()