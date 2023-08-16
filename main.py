import json
from datetime import datetime
import os


def is_default(x):
    return len(x) == 0


def add_money(pos):
    tabs = get_tabs()
    while True:
        money_in = input("How much do you want to add (default: go back)? ")
        if is_default(money_in):
            return dashboard(pos)

        title = input("What's the title of this transaction (default: go back)? ")
        if not is_default(title):
            tabs[pos]["current balance"] += float(money_in)

            tabs[pos]["expenses"].append({"title": title, "money": f"+ {money_in}"})
            save_tabs(tabs)
            dashboard(pos)
            break


def add_expense(pos):
    tabs = get_tabs()
    while True:
        money_in = input("How much do you want to add (default: go back)? ")
        if is_default(money_in):
            return dashboard(pos)

        title = input("What's the title of this transaction (default: go back)? ")
        if not is_default(title):
            tabs[pos]["current balance"] -= float(money_in)

            tabs[pos]["expenses"].append({"title": title, "money": f"- {money_in}"})
            save_tabs(tabs)
            dashboard(pos)
            break


def save_tabs(tabs):
    file = open(f"storage/tabs.json", "w")
    file.write(json.dumps(tabs))
    file.close()


def dashboard(pos):
    tabs = get_tabs()
    tab_name = tabs[pos]["name"]
    current_balance = tabs[pos]["current balance"]
    print(f"Dashboard:\n\tName: {tab_name}\n\tBalance: {current_balance}")
    print(
        "\nWhat do you want to do\n"
        "1. Add expense.\n"
        "2. Add money.\n"
        "3. Go back.\n"
        "4. Close application.\n"
    )

    while True:
        res = input("Your response (1 ~ 5): ").strip()

        if res == "1":
            add_expense(pos)
            break
        elif res == "2":
            add_money(pos)
            break
        elif res == "3":
            print("Okay then...")
            main()
            break
        elif res == "4":
            print("Closing...")
            exit(0)
        else:
            print("Invalid response!")


def create_tab():
    tab_name = input("Creating a new tab. What will the name be (default: cancel): ")
    if len(tab_name.strip()) == 0:
        return main()

    tabs = get_tabs()
    tabs.append(
        {
            "name": tab_name,
            "created": datetime.now().timestamp(),
            "current balance": 0,
            "expenses": [],
        }
    )

    save_tabs(tabs)

    print("Got it! Let's go to the dashboard")
    dashboard(len(tabs) - 1)


def get_tabs():
    file = open(f"storage/tabs.json", "r")
    tabs = json.loads(file.read())
    return tabs


def display_tabs():
    tabs = get_tabs()
    if len(tabs) == 0:
        return "\tNothing to see here."

    return "\n".join([f"\t{i + 1}. {tabs[i]['name']}" for i in range(0, len(tabs))])


def select_tab():
    tabs = get_tabs()
    if len(tabs) == 0:
        print("There are no tabs to select")
        return main()
    elif len(tabs) == 1:
        while True:
            res = (
                input("You have only one tab. Do you wanna view it? (Y/n)")
                .strip()
                .lower()
            )
            if len(res) == 0 or res == "y":
                return dashboard(0)
            else:
                return main()
    else:
        response = input(f"Your response( 1 ~ {len(tabs)} | default: cancel): ")
        if len(response.strip()) == 0:
            return main()
        else:
            dashboard(int(response) - 1)


def delete(pos):
    print(f"Deleting tab {pos + 1}")
    tabs = get_tabs()
    del tabs[pos]
    save_tabs(tabs)


def delete_tab():
    tabs = get_tabs()
    if len(tabs) == 0:
        print("There are no tabs to delete")
        return main()
    elif len(tabs) == 1:
        while True:
            res = (
                input("You have only one tab. Do you wanna delete it? (y/N): ")
                .strip()
                .lower()
            )
            if res == "y":
                return delete(0)
            return main()
    else:
        response = input(
            f"Which tab do you wanna delete ( 1 ~ {len(tabs)} | default: cancel): "
        )
        if len(response.strip()) != 0:
            delete(int(response) - 1)
        return main()


def main():
    print(f"Your tabs:\n{display_tabs()}\n\n\n")
    print(
        "Do you want to:\n"
        "1. Create a tab.\n"
        "2. Select a tab.\n"
        "3. Delete a tab.\n"
        "4. Delete all tabs.\n"
        "5. Close application.\n\n"
    )

    while True:
        res = input("Your response (1 ~ 5): ").strip()

        if res == "1":
            create_tab()
            break
        elif res == "2":
            select_tab()
            break
        elif res == "3":
            delete_tab()
            break
        elif res == "4":
            print("Resetting...")
            save_tabs([])
            dashboard()
            break
        elif res == "5":
            print("Closing...")
            exit(0)
        else:
            print("Invalid response!")


if __name__ == "__main__":
    if not os.path.exists("storage/"):
        os.mkdir("storage")
        if not os.path.exists("storage/tabs.json"):
            save_tabs([])
    main()
