import json
import os
from datetime import datetime, timedelta
from uptils.clearterminal import clear_terminal
from uptils import colors


STREAKS_FILE = os.path.join(colors.notes_file, 'streaks.json')
SAVEDDATE = os.path.join(colors.notes_file, 'streakdate.json')

# Initialize the list of streaks
streaks = []

def reset_today_flags():
    load_streaks()

    for streak in streaks:
        streak['today'] = False

    save_streaks()  # Save the updated streak data
    print("All streaks marked as not completed for today.")

def save_todays_date():
    # Get today's date in the format 'dd-mm-yyyy'
    today_date = datetime.today().date().strftime("%d-%m-%Y")

    # Save today's date to a JSON file
    with open(SAVEDDATE, 'w') as f:
        json.dump(today_date, f)

def load_todays_date():
    try:
        with open(SAVEDDATE, 'r') as f:
            saved_date_str = json.load(f)
            return datetime.strptime(saved_date_str, "%d-%m-%Y").date()
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or there's an issue with JSON decoding, return None
        save_todays_date()
        return None


# Load streak data from file (if available)
def load_streaks():
    global streaks  
    if os.path.exists(STREAKS_FILE):
        with open(STREAKS_FILE, "r") as f:
            streaks = json.load(f)

# Function to save streak data to a file
def save_streaks():
    global streaks  
    with open(STREAKS_FILE, "w") as f:
        json.dump(streaks, f, indent=4)


def complete_streak_for_today():
    clear_terminal()
    show_streaks()

    choice = input("\nEnter the number of the streak to complete for today: ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(streaks):
            streak = streaks[choice - 1]
            streak['today'] = True
            streak['count'] += 1
            save_streaks()
            clear_terminal()
            print(f"{streak['name']} streak marked as completed for today.")
        else:
            clear_terminal()
            print("Invalid streak number.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

def show_streaks():
    load_streaks()
    if not streaks:
        print("\n\nNo streaks to display.")
    else:
        current_date = datetime.now().date()
        print(f"\n\n{colors.space*7}{colors.CYAN}Today\n{colors.space*7}{colors.line2*50}{colors.RESET}")
        for i, streak in enumerate(streaks, start=1):
            attention_message = " - needs attention" if not streak.get('today', False) else ""
            print(f"{colors.space*7} {colors.GREEN} {i}. {colors.YELLOW}{streak['name']} {colors.GREEN}({streak['count']}){colors.BLUE}{attention_message}{colors.RESET}")

def add_streak():
    load_streaks()
    clear_terminal()
    name = input("\nEnter streak name: ")
    new_streak = {
        'name': name,
        'count': 0,
        'today': False, 
        'last_checked': str(datetime.now().date())
    }
    streaks.append(new_streak)
    save_streaks()
    clear_terminal()
    print(f"{name} streak added successfully.")

# Function to remove a streak
def remove_streak():
    clear_terminal()
    show_streaks()
    choice = input("\nEnter the number of the streak to remove: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(streaks):
            removed_streak = streaks.pop(choice - 1)
            save_streaks()
            clear_terminal()
            print(f"{removed_streak['name']} streak removed.")
        else:
            clear_terminal()
            print("Invalid streak number.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")


def auto_reset_streaks():
    load_streaks()
    saved_date = load_todays_date()

    # Get today's date in the format 'dd-mm-yyyy'
    today_date = datetime.today().date()  # Fix: Use datetime.today().date() instead of datetime.date.today()

    if saved_date == today_date:
        return 

    current_date = datetime.now().date()

    for streak in streaks:
        if not streak['today']:
            streak['count'] = 0
            streak['last_checked'] = str(current_date)

    save_streaks()
    reset_today_flags()
    save_todays_date()
    print("WOAH, someone did NOT do their job LOL")

def flush_streaks():
    load_streaks()
    global streaks  # Access the global streaks list
    clear_terminal()
    choice = input("Are You sure?(y/n)")
    if choice.lower == "y":
        streaks = []  # Clear all streaks
        save_streaks()  # Save the empty list to the streak data file
        print("Streak database flushed.")
    else:
        clear_terminal()

# Main program loop
def main():
    auto_reset_streaks()
    while True:
        print(f"\n{colors.WPURPLE}||Streak Tracker/Habit Formation||\n{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET}{colors.YELLOW} Show Streaks{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET}{colors.YELLOW} Add Streak{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET}{colors.YELLOW} Remove Streak{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET}{colors.YELLOW} Check Streak{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET}{colors.YELLOW} flush streak database{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET}{colors.YELLOW} Quit{colors.RESET}")
        choice = input("\nEnter your choice: ")

        if choice == 's':
            clear_terminal()
            show_streaks()
            input(f"{colors.YELLOW}\n{colors.space*5}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == 'a':
            add_streak()
        elif choice == 'r':
            remove_streak()
        elif choice == 'c':
            complete_streak_for_today()
        elif choice == 'f':
            flush_streaks()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()
