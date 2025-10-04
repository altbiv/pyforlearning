"""
CLI Based Habit Tracker
"""

from pathlib import Path
import json
from datetime import date, datetime
import sys

DATA_FILE = Path("habits.json")
GOAL_DAYS = 21

def load_data():
    if not DATA_FILE.exists():
        return {"habits": {}}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"habits": {}}

def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def iso_today():
    return date.today().isoformat()

def add_habit(data):
    name = input("Enter new habit name (e.g. 'Meditate'): ").strip()
    if not name:
        print("No name entered. Returning to menu.")
        return

    key = name.lower()
    if key in data["habits"]:
        print(f"'{name}' already exists. Try checking in instead.")
        return

    habit = {
        "name": name,
        "created": iso_today(),
        "checks": [],       
        "completed": False
    }
    data["habits"][key] = habit
    save_data(data)
    print(f"Habit '{name}' added. Go crush those 21 days! 🎯")

def list_habits(data):
    habits = data.get("habits", {})
    if not habits:
        print("No habits yet — add one from the menu.")
        return []
    keys = sorted(habits.keys())
    for i, k in enumerate(keys, 1):
        h = habits[k]
        days = len(h.get("checks", []))
        status = "✅ Completed" if h.get("completed", False) else f"{days}/{GOAL_DAYS} days"
        print(f"{i}. {h['name']}  —  {status}")
    return keys

def choose_habit(data):
    keys = list_habits(data)
    if not keys:
        return None
    try:
        choice = input("\nChoose habit number (or press Enter to cancel): ").strip()
        if choice == "":
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(keys):
            return keys[idx]
    except ValueError:
        pass
    print("Invalid selection.")
    return None

def checkin(data):
    key = choose_habit(data)
    if not key:
        return
    habit = data["habits"][key]
    today = iso_today()

    if habit.get("completed", False):
        print(f"'{habit['name']}' is already completed. 🎉")
        return

    if today in habit["checks"]:
        print(f"You already checked in for '{habit['name']}' today. Nice consistency! 💪")
        return

    habit["checks"].append(today)

    if len(habit["checks"]) >= GOAL_DAYS:
        habit["completed"] = True
        print(f"🎊 Congrats! You completed '{habit['name']}' — {GOAL_DAYS} days done!")
    else:
        remaining = GOAL_DAYS - len(habit["checks"])
        percent = (len(habit["checks"]) / GOAL_DAYS) * 100
        print(f"Checked in for '{habit['name']}'. Progress: {len(habit['checks'])}/{GOAL_DAYS} ({percent:.1f}%). {remaining} days to go.")

    save_data(data)

def show_details(data):
    key = choose_habit(data)
    if not key:
        return
    h = data["habits"][key]
    checks = h.get("checks", [])
    print(f"\nName     : {h['name']}")
    print(f"Created  : {h.get('created')}")
    print(f"Completed: {h.get('completed')}")
    print(f"Days     : {len(checks)}/{GOAL_DAYS}")
    if checks:
        print("Checks   :", ", ".join(checks[-10:]))
    else:
        print("Checks   : (none yet)")
    print()

def delete_habit(data):
    key = choose_habit(data)
    if not key:
        return
    name = data["habits"][key]["name"]
    confirm = input(f"Type 'yes' to delete habit '{name}': ").strip().lower()
    if confirm == "yes":
        del data["habits"][key]
        save_data(data)
        print(f"Deleted '{name}'.")
    else:
        print("Not deleted.")

def main_menu():
    data = load_data()
    menu = """
Habit Tracker — 21 Day Challenge
-------------------------------
1) Add new habit
2) Check in for habit (today)
3) Show habits
4) Habit details
5) Delete habit
6) Exit
"""
    while True:
        print(menu)
        choice = input("Pick an option (1-6): ").strip()
        if choice == "1":
            add_habit(data)
        elif choice == "2":
            checkin(data)
        elif choice == "3":
            list_habits(data)
        elif choice == "4":
            show_details(data)
        elif choice == "5":
            delete_habit(data)
        elif choice == "6":
            print("Stay consistent — you've got this! 👊")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nBye — keep building good habits! 👋")
        sys.exit(0)
