from app.accounts import create_account


def main():
    customer_id = int(input("Customer ID: "))
    account_type = input(
        "Account type (SAVINGS/CURRENT): "
    ).strip().upper()

    create_account(customer_id, account_type)


if __name__ == "__main__":
    main()