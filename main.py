import json
from datetime import datetime
import os


def dashboard(pos):
    tabs = get_tabs()
    tab_name = tabs[pos]["name"]
    print(f"Dashboard: {tab_name}")
    print(
        "\nWhat do you want to do\n"
        "1. Add expense.\n"
        "2. Check balance.\n"
        "3. Check expenses.\n"
        "4. Go back.\n"
        "5. Close application.\n"
    )

    while True:
        res = input("Your response (1 ~ 5): ").strip()

        if res == "1":
            # add expense
            break
        elif res == "2":
            # check balance
            break
        elif res == "3":
            # check expenses
            break
        elif res == "4":
            print("Okay then...")
            main()
            break
        elif res == "5":
            print("Closing...")
            exit(0)
        else:
            print("Invalid response!")


def create_tab():
    tab_name = input(
        'Creating a new tab. What will the name be (enter "c" to cancel): '
    )
    if tab_name.strip() == "c":
        return main()

    tabs = get_tabs()
    tabs.append({"name": tab_name, "created": datetime.now().timestamp()})

    file = open(f"storage/tabs.json", "w")
    file.write(json.dumps(tabs))
    file.close()

    print("Got it! Let's go to the dashboard")
    dashboard(len(tabs) - 1)


def reset_tabs():
    file = open(f"storage/tabs.json", "w")
    file.write("[]")
    file.close()


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
                dashboard(0)
            else:
                main()
    else:
        response = input(f'Your response( 1 ~ {len(tabs)} ) (enter "c" to cancel): ')
        if response.strip() == "c":
            return main()
        else:
            dashboard(int(response) - 1)


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
            # Delete a tab
            break
        elif res == "4":
            print("Resetting...")
            reset_tabs()
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
            reset_tabs()
    main()
