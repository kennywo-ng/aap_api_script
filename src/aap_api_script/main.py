from functions import func_1, func_2, func_3, func_4

def main():
    print("""
    1. Print inventory hosts with inventory names
    2. Compare hosts from excel with inventory hosts
    3. Bulk import hosts to inventory
    4. Group hosts
    """)

    choice = input("Enter your choice: ")

    actions = {
        "1": func_1,
        "2": func_2,
        "3": func_3,
        "4": func_4
    }

    action = actions.get(choice)

    if action:
        action()
    else:
        print("Invalid choice")
        main()

if __name__ == "__main__":
    main()
