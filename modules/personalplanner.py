from datetime import datetime, timedelta
import numpy as np
import json, random, os, re, math
from uptils.clearterminal import clear_terminal
from uptils import colors

current_day = datetime.now().weekday()
adjusted_day_index = (current_day +2) % 7
TOODO_TXT = os.path.join(colors.notes_file, 'Jobtodot.txt')
TASKDB = os.path.join(colors.notes_file, 'PersonalTasksI.json')
ARCHIVEDB = os.path.join(colors.notes_file, 'ArchivedTasksI.json')
RECENTHOUR = os.path.join(colors.notes_file, 'recent_hour_task.json')
TASKCOUNT = os.path.join(colors.notes_file, 'task_count.json')


def edit_notes(vsc=False):
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\jobtodot.txt"
        editor = 'notepad'
    else:
        try:
            notes_file = os.path.expanduser("./Jobtodot.txt")
            if vsc == True:
                editor = 'geany'
            else:
                editor = 'nvim'
            os.system(f"{editor} {notes_file}")
        except:
            print("wrong number")

def create_empty_files():
    if not os.path.exists(TOODO_TXT):
        with open(TOODO_TXT, 'w') as file:
            # Write the weekday names and task placeholders for each day
            for day in ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                file.write(f"{day}\n")
                file.write("---------\n")
                for hour in range(5,24):
                    file.write(f"{hour} - \n")
                file.write("\n")
    if not os.path.exists(TASKDB):
        with open(TASKDB, 'w') as file:
            json.dump([], file)
    if not os.path.exists(ARCHIVEDB):
        with open(ARCHIVEDB, 'w') as file:
            json.dump([], file)
    if not os.path.exists(RECENTHOUR):
        with open(RECENTHOUR, 'w') as file:
            json.dump(0, file)


def add_task(task_description):
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        data.append(task_description)
        file.seek(0)
        json.dump(data, file, indent=4)

def show_current_task():
    with open(TASKDB, 'r') as file:
        data = json.load(file)
        if data:
            print(f"{colors.YELLOW}   Current Task:{colors.RESET}")
            print(f"{colors.space*7}{colors.WPURPLE}{data[0]}{colors.RESET}")
        else:
            print("No tasks in the stack.")

def show_task_stack():
    with open(TASKDB, 'r') as file:
        data = json.load(file)
        if data:
            clear_terminal()
            print("\n\nTask Stack")
            for i, task in enumerate(data, 1):
                print(f"{i}. {task}")
        else:
            clear_terminal()
            print("No tasks in the stack.")
        input("press any key to continue....")

def accomplish_task():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        if data:
            completed_task = data.pop(0)
            file.seek(0) 
            file.truncate()  
            json.dump(data, file, indent=4) 
            clear_terminal()
            print(f"Task '{completed_task}' accomplished and removed from the stack.")
        else:
            clear_terminal()
            print("No tasks to accomplish.")

def postpone_task():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        if len(data) >= 3:  
            top_task = data.pop(0)  
            data.insert(2, top_task)  
            file.seek(0) 
            file.truncate() 
            json.dump(data, file, indent=4)  
            clear_terminal()
            print(f"Task '{top_task}' postponed and moved down.")
        else:
            clear_terminal()
            print("Not enough tasks to postpone.")

def change_task_placement():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        if data:
            clear_terminal()
            print("\n\nTask Stack")
            for i, task in enumerate(data, 1):
                print(f"{i}. {task}")
            print()
            choice_task_index = input("Enter the index of the task you want to change placement: ")
            choice_placement_index = input("Enter the index where you want to place the task: ")
            try:
                task_index = int(choice_task_index) - 1
                placement_index = int(choice_placement_index)
                if 0 <= task_index < len(data) and 0 <= placement_index <= len(data):
                    task = data.pop(task_index)
                    data.insert(placement_index-1, task)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
                    print(f"Task '{task}' moved to index {placement_index} of the stack.")
                else:
                    print("Invalid index. Please enter valid indices.")
            except ValueError:
                print("Invalid input. Please enter valid indices.")
        else:
            clear_terminal()
            print("No tasks in the stack.")
            input("Press any key to continue...")


def custom_postpone():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        post_numb = int(input("what interval do you want to postpone? "))
        if len(data) >= post_numb-1:  
            top_task = data.pop(0)
            data.insert(post_numb, top_task)  
            file.seek(0) 
            file.truncate() 
            json.dump(data, file, indent=4)  
            clear_terminal()
            print(f"Task '{top_task}' postponed and moved down.")
        else:
            clear_terminal()
            print("Not enough tasks to postpone.")

def archive_or_reactivate():
    choice = input("Do you want to archive or reactivate tasks? (a/r): ").lower()
    if choice == "a":
        archive_task()
    elif choice == "r":
        reactivate_task()
    else:
        print("Invalid choice. Please enter 'a' for archive or 'r' for reactivate.")

def archive_task():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        if data:
            top_task = data.pop(0)  # Remove the top task
            with open(ARCHIVEDB, 'r+') as archive_file:
                archived_data = json.load(archive_file)
                archived_data.append(top_task)
                archive_file.seek(0)  # Move the cursor to the beginning of the file
                archive_file.truncate()  # Clear the file contents
                json.dump(archived_data, archive_file, indent=4)  # Write the updated data to the file
            file.seek(0)  # Move the cursor to the beginning of the file
            file.truncate()  # Clear the file contents
            json.dump(data, file, indent=4)  # Write the updated data to the file
            print(f"Task '{top_task}' archived successfully.")
        else:
            print("No tasks to archive.")

def reactivate_task():
    with open(ARCHIVEDB, 'r+') as archive_file:
        archived_data = json.load(archive_file)
        if archived_data:
            print("Archived Tasks:")
            for i, task in enumerate(archived_data, 1):
                print(f"{i}. {task}")
            choice = input("Select a task to reactivate: ")
            try:
                choice_index = int(choice) - 1
                selected_task = archived_data.pop(choice_index)
                with open(TASKDB, 'r+') as file:
                    data = json.load(file)
                    data.append(selected_task)
                    file.seek(0)  # Move the cursor to the beginning of the file
                    file.truncate()  # Clear the file contents
                    json.dump(data, file, indent=4)  # Write the updated data to the file
                with open(ARCHIVEDB, 'w') as archive_file:
                    json.dump(archived_data, archive_file, indent=4)  # Write the updated data back to the ARCHIVEDB
                print(f"Task '{selected_task}' reactivated and added to the stack.")
            except (ValueError, IndexError):
                print("Invalid choice. Task reactivation canceled.")
        else:
            print("No archived tasks.")

def read_todo_txt():
    current_day_name = datetime.now().strftime("%A")
    current_hour = datetime.now().hour
    recent_hour = get_recent_hour()
    
    if recent_hour == current_hour:
        clear_terminal()
        print("\nTask for the current hour has already been accounted for.\n\n")
        return

    with open(TOODO_TXT, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip() == current_day_name:
                hour_index = i + 2  # Skip the dashed line
                hour_task_pairs = lines[hour_index:]
                for pair in hour_task_pairs:
                    try:
                        hour, task = pair.split(" - ", 1)
                    except ValueError:
                        store_recent_hour(current_hour)
                        return
                    if int(hour) == current_hour and task.strip():
                        print(task.startswith)
                        add_task_to_second_place(task.strip())
                        store_recent_hour(current_hour)
                        return 
        print("No task scheduled for the current hour.")


def add_task_to_second_place(task_description):
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        data.insert(1, task_description)
        file.seek(0)
        json.dump(data, file, indent=4)

def store_recent_hour(hour):
    with open(RECENTHOUR, "w") as file:
        file.write(str(hour))

def get_recent_hour():
    try:
        with open(RECENTHOUR, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return None

def get_top_task():
    with open(TASKDB, 'r') as file:
        data = json.load(file)
        if data:
            return data[0]
        else:
            return None

def bring_task_to_top():
    with open(TASKDB, 'r+') as file:
        data = json.load(file)
        if data:
            clear_terminal()
            print("\n\nTask Stack")
            for i, task in enumerate(data, 1):
                print(f"{i}. {task}")
            print()
            choice = input("Enter the index of the task you want to bring to the top: ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(data):
                    task = data.pop(index)
                    data.insert(0, task)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
                    print(f"Task '{task}' moved to the top of the stack.")
                else:
                    print("Invalid index. Please enter a valid index.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            clear_terminal()
            print("No tasks in the stack.")
            input("Press any key to continue...")

def count_tasks_and_write_to_json():
    with open(TASKDB, 'r') as file:
        data = json.load(file)
        task_count = len(data)

    # Write task count to a new JSON file
    task_count_data = {"task_count": task_count}
    with open(TASKCOUNT, 'w') as count_file:
        json.dump(task_count_data, count_file, indent=4)

    print(f"Total number of tasks: {task_count}")

def main():
    clear_terminal()
    print("\n\n")
    create_empty_files()
    while True:
        read_todo_txt()
        show_current_task()
        print("\n\n")
        print(f"\n{colors.YELLOW}||Personal Scheduler||{colors.RESET}\n")
        print(f"{colors.CYAN}n.{colors.RESET}{colors.YELLOW}Add a task{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET}{colors.YELLOW}Accomplish task{colors.RESET}")
        print(f"{colors.CYAN}p.{colors.RESET}{colors.YELLOW}Postpone current task{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET}{colors.YELLOW}custom Postpone task{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET}{colors.YELLOW}List the stack{colors.RESET}")
        print(f"{colors.CYAN}e.{colors.RESET}{colors.YELLOW}Edit Schedule{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET}{colors.YELLOW}Select to do a task Now{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET}{colors.YELLOW}Modify Task on Stack{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET}{colors.YELLOW}Archive/Active to stack{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET}{colors.YELLOW}Exit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "a":
            accomplish_task()
            count_tasks_and_write_to_json()
        elif choice == "n":
            clear_terminal()
            task_description = input(f"\n{colors.YELLOW}Enter task description:{colors.RESET} ")
            add_task(task_description)
            count_tasks_and_write_to_json()
        elif choice == "p":
            postpone_task()
        elif choice == "d":
            bring_task_to_top()
        elif choice == "m":
            change_task_placement()
        elif choice == "c":
            custom_postpone()
        elif choice == "l":
            show_task_stack()
            clear_terminal()
        elif choice == "e":
            edit_notes()
            clear_terminal()
        elif choice == "ee":
            edit_notes(vsc=True)
            clear_terminal()
        elif choice == "r":
            archive_or_reactivate()
            clear_terminal()
        elif choice == "d":
            read_todo_txt()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == "__main__":
    main()