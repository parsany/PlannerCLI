from datetime import datetime, timedelta
import json, random, os, re, math

current_day = datetime.now().weekday()
adjusted_day_index = (current_day +2) % 7

dirn = ".plannerconf"
notes_file = os.path.join(os.getcwd(), dirn)
TOODO_TXT = os.path.join(notes_file, 'Jobtodot.txt')
TASKDB = os.path.join(notes_file, 'PersonalTasksI.json')
ARCHIVEDB = os.path.join(notes_file, 'ArchivedTasksI.json')
RECENTHOUR = os.path.join(notes_file, 'recent_hour_task.json')
TASKCOUNT = os.path.join(notes_file, 'task_count.json')


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

def read_todo_txt():
    current_day_name = datetime.now().strftime("%A")
    current_hour = datetime.now().hour
    recent_hour = get_recent_hour()
    
    if recent_hour == current_hour:
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
                        add_task_to_second_place(task.strip())
                        store_recent_hour(current_hour)
                        return 


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

def count_tasks_and_write_to_json():
    with open(TASKDB, 'r') as file:
        data = json.load(file)
        task_count = len(data)

    # Write task count to a new JSON file
    task_count_data = {"task_count": task_count}
    with open(TASKCOUNT, 'w') as count_file:
        json.dump(task_count_data, count_file, indent=4)

def main():
    create_empty_files()
    read_todo_txt()
    count_tasks_and_write_to_json()
        

if __name__ == "__main__":
    main()