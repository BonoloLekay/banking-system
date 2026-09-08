from app.customers import create_customer
from app.accounts import create_account
from app.transactions import deposit, withdraw, transfer


def display_menu():
    print("\n" + "=" * 40)
    print("          BANKING SYSTEM")
    print("=" * 40)
    print("1. Create Customer")
    print("2. Create Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer Money")
    print("6. Exit")
    print("=" * 40)


def main():
    while True:
        display_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            id_number = input("ID number: ").strip()

            create_customer(
                first_name,
                last_name,
                email,
                phone,
                id_number
            )

        elif choice == "2":
            try:
                customer_id = int(input("Customer ID: "))
                account_type = input(
                    "Account type (SAVINGS/CURRENT): "
                ).strip().upper()

                create_account(customer_id, account_type)

            except ValueError:
                print("Customer ID must be a number.")

        elif choice == "3":
            try:
                account_id = int(input("Account ID: "))
                amount = input("Deposit amount: ")

                deposit(account_id, amount)

            except ValueError:
                print("Account ID must be a number.")

        elif choice == "4":
            try:
                account_id = int(input("Account ID: "))
                amount = input("Withdrawal amount: ")

                withdraw(account_id, amount)

            except ValueError:
                print("Account ID must be a number.")

        elif choice == "5":
            try:
                from_account_id = int(
                    input("From Account ID: ")
                )

                to_account_id = int(
                    input("To Account ID: ")
                )

                amount = input("Transfer amount: ")

                transfer(
                    from_account_id,
                    to_account_id,
                    amount
                )

            except ValueError:
                print("Account IDs must be numbers.")

        elif choice == "6":
            print("Thank you for using the Banking System.")
            break

        else:
            print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()