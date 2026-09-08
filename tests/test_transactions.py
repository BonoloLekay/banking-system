from decimal import Decimal
from app.transactions import deposit, withdraw, transfer
from app.database import get_connection



def reset_test_data():
    connection = get_connection(testing=True)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM accounts")
    cursor.execute("DELETE FROM customers")

    connection.commit()

    cursor.close()
    connection.close()


def create_test_account(balance=Decimal("1000.00")):
    connection = get_connection(testing=True)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (
            first_name,
            last_name,
            email,
            phone,
            id_number
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            "Test",
            "Customer",
            "test@example.com",
            "0712345678",
            "0000000000000"
        )
    )

    customer_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO accounts (
            customer_id,
            account_number,
            account_type,
            balance
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            customer_id,
            "TEST100001",
            "SAVINGS",
            balance
        )
    )

    account_id = cursor.lastrowid

    connection.commit()

    cursor.close()
    connection.close()

    return account_id

def test_deposit_updates_balance():
    reset_test_data()

    account_id = create_test_account(
        Decimal("1000.00")
    )

    deposit(
        account_id,
        "500",
        testing=True
    )

    connection = get_connection(testing=True)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM accounts
        WHERE account_id = %s
        """,
        (account_id,)
    )

    balance = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert balance == Decimal("1500.00")

def get_balance(account_id):
    connection = get_connection(testing=True)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM accounts
        WHERE account_id = %s
        """,
        (account_id,)
    )

    balance = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return balance


def test_withdraw_reduces_balance():
    reset_test_data()

    account_id = create_test_account(
        Decimal("1000.00")
    )

    withdraw(
        account_id,
        "300",
        testing=True
    )

    assert get_balance(account_id) == Decimal("700.00")


def test_withdraw_rejects_insufficient_funds():
    reset_test_data()

    account_id = create_test_account(
        Decimal("500.00")
    )

    withdraw(
        account_id,
        "1000",
        testing=True
    )

    assert get_balance(account_id) == Decimal("500.00")


def test_negative_deposit_does_not_change_balance():
    reset_test_data()

    account_id = create_test_account(
        Decimal("1000.00")
    )

    deposit(
        account_id,
        "-500",
        testing=True
    )

    assert get_balance(account_id) == Decimal("1000.00")


def test_negative_withdrawal_does_not_change_balance():
    reset_test_data()

    account_id = create_test_account(
        Decimal("1000.00")
    )

    withdraw(
        account_id,
        "-200",
        testing=True
    )

    assert get_balance(account_id) == Decimal("1000.00")


def create_second_test_account(
    balance=Decimal("0.00")
):
    connection = get_connection(testing=True)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (
            first_name,
            last_name,
            email,
            phone,
            id_number
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            "Second",
            "Customer",
            "second@example.com",
            "0723456789",
            "1111111111111"
        )
    )

    customer_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO accounts (
            customer_id,
            account_number,
            account_type,
            balance
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            customer_id,
            "TEST200002",
            "CURRENT",
            balance
        )
    )

    account_id = cursor.lastrowid

    connection.commit()

    cursor.close()
    connection.close()

    return account_id


def test_transfer_moves_money_between_accounts():
    reset_test_data()

    sender_id = create_test_account(
        Decimal("1000.00")
    )

    receiver_id = create_second_test_account(
        Decimal("200.00")
    )

    transfer(
        sender_id,
        receiver_id,
        "300",
        testing=True
    )

    assert get_balance(sender_id) == Decimal("700.00")
    assert get_balance(receiver_id) == Decimal("500.00")


def test_transfer_rejects_insufficient_funds():
    reset_test_data()

    sender_id = create_test_account(
        Decimal("100.00")
    )

    receiver_id = create_second_test_account(
        Decimal("200.00")
    )

    transfer(
        sender_id,
        receiver_id,
        "500",
        testing=True
    )

    assert get_balance(sender_id) == Decimal("100.00")
    assert get_balance(receiver_id) == Decimal("200.00")


def test_transfer_rejects_same_account():
    reset_test_data()

    account_id = create_test_account(
        Decimal("1000.00")
    )

    transfer(
        account_id,
        account_id,
        "200",
        testing=True
    )

    assert get_balance(account_id) == Decimal("1000.00")