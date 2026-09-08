from app.transactions import withdraw


def main():
    try:
        account_id = int(input("Account ID: "))
        amount = input("Withdrawal amount: ")

        withdraw(account_id, amount)

    except ValueError:
        print("Account ID must be a number.")


if __name__ == "__main__":
    main()