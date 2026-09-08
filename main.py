from app.transactions import transfer


def main():
    try:
        from_account_id = int(input("From Account ID: "))
        to_account_id = int(input("To Account ID: "))
        amount = input("Transfer amount: ")

        transfer(
            from_account_id,
            to_account_id,
            amount
        )

    except ValueError:
        print("Account IDs must be numbers.")


if __name__ == "__main__":
    main()