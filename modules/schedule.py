import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from uptils.clearterminal import clear_terminal
from uptils import colors
from estimations import estimation, bookplanner, lectureplanner, xestimation, freeplanner, goalplanner
import json, random, os, re, math
from modules import reminder, personalplanner

current_day = datetime.now().weekday()
day_names = {
    0: 'MON',
    1: 'TUE',
    2: 'WED',
    3: 'THUR',
    4: 'FRI',
    5: 'SAT',
    6: 'SUN'
}


SCH_TXT = os.path.join(colors.notes_file, 'plan.md')
JOB_TXT = os.path.join(colors.notes_file, 'jobtodo.txt')
JobDB = os.path.join(colors.notes_file, 'jobdo.json')
TIMEJC = os.path.join(colors.notes_file, 'timejc.json')
EBDB = os.path.join(colors.notes_file, 'endeavors.json')
TMPBOX = os.path.join(colors.notes_file, 'tempbox.json')
TAGS_FILE = os.path.join(colors.notes_file, 'tags.json')
SEVEN_DAYS_FILE = os.path.join(colors.notes_file, '7days.json')
total_hours = 0


def remove_color_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def edit_notes(files):
    if os.name == 'nt':
        filechoose = int(input(f"\n{colors.YELLOW}||list||\n\n{colors.YELLOW}1-3.schedule\n{colors.YELLOW}2-4.job\n{colors.YELLOW}0.notes\n\n{colors.WWITE}select the one you want to edit: "))
        if filechoose == 1:
            notes_file = "C:\\Program Files\\Planner\\plan.md"
        else:
            notes_file = "C:\\Program Files\\Planner\\jobtodo.txt"
        editor = 'notepad'
    else:
        if files == True:
            notes_file = os.path.expanduser("./schednotes.txt")
            editor = 'nvim'
        else:
            filechoose = int(input(f"\n{colors.YELLOW}||list||\n\n{colors.YELLOW}1-3.schedule\n{colors.YELLOW}2-4.job\n{colors.YELLOW}0.notes\n\n{colors.WWITE}select the one you want to edit: "))
            try:
                if filechoose == 1:
                    notes_file = os.path.expanduser("./plan.md")
                    editor = 'nvim'
                elif filechoose == 2:
                    notes_file = os.path.expanduser("./jobtodo.txt")
                    editor = 'nvim'
                elif filechoose == 3:
                    notes_file = os.path.expanduser("./plan.md")
                    editor = 'vscodium'
                elif filechoose == 4:
                    notes_file = os.path.expanduser("./jobtodo.txt")
                    editor = 'vscodium'
                elif filechoose == 0:
                    notes_file = os.path.expanduser("./schednotes.txt")
                    editor = 'nvim'
                os.system(f"{editor} {notes_file}")
            except:
                print("wrong number")
    


def show_schedule_by_time(print_output):
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    activities_found = False  
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if start_time <= current_time <= end_time:
            if not activity == "free time":
                activities_found = True
            if print_output == True:
                try:
                    with open(JobDB, 'r') as file:
                        data = json.load(file)
                        tasks = data.get('tasks', [])
                        if tasks:
                            first_entry = tasks[0]
                except:
                    pass
                print(f"{colors.space*7}{colors.CYAN}got scheduled activity: {colors.WPURPLE}{line}{colors.PURPLE} /{personalplanner.get_top_task()}{colors.RESET}") 
            return activities_found
            
    if print_output == True and not activities_found:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")
        return False




def get_schedule_output(lastl):
    global total_hours
    output = []
    free_activities_hours = {}

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    print_schedule = False
    for line in lines:
        line = line.strip()
        if line.startswith('#') and day_names[current_day] in line:
            current_day_name = day_names[current_day]
            print_schedule = True
            output.append(f"{colors.CYAN} {line}{colors.RESET}")
            free_activities_hours[current_day_name] = 0  
        elif print_schedule and line:
            if line.endswith('*'):
                output.append(f"{colors.space*2}{colors.WPURPLE}{line}{colors.RESET}")
            elif line.endswith('course studies'):
                output.append(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('$'):
                output.append(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('free'):
                output.append(f"{colors.space*2}{colors.YELLOW}{line}{colors.RESET}")
            else:
                output.append(f"{colors.space*2}{colors.BLUE}{line}{colors.RESET}")

            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free time":
                free_activities_hours[current_day_name] += activity_hours

        elif print_schedule and not line:
            break
    
    if lastl:
        for day, total_hours in free_activities_hours.items():
            output.append(f"{colors.space*2}{colors.WPURPLE}{day} - Total Free Hours: {total_hours:.2f} hours{colors.RESET}")
            workperday = estimation.tracker_greedy(rint=False)
            output.append(f"\n{colors.space*2}{colors.CYAN}📕Amount of work predicted for today: {calculate_work('work')*total_hours:.2f}{colors.RESET}")
            output.append(f"{colors.space*2}{colors.CYAN}📒Amount of books predicted for today: {calculate_work('book')*total_hours:.2f}{colors.RESET}")
            output.append(f"{colors.space*2}{colors.CYAN}📼Amount of videos: {calculate_work('videos')*total_hours:.2f} minutes #tasks {colors.RESET}")
            output.append(colors.space*2+f" {colors.YELLOW}[watch over endeavors in break times.]")

    return '\n'.join(output)


def parse_schedule(JobDB):
    schedule = {}
    with open(JobDB, 'r') as file:
        lines = file.readlines()
        current_day = None
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                current_day = line[2:]
                schedule[current_day] = []
            elif line:  
                start_time, end_time, activity = line.split(' - ')
                schedule[current_day].append((start_time.strip(), end_time.strip(), activity.strip()))
    return schedule


def plot_schedule():
    schedule = parse_schedule(SCH_TXT)
    days = list(schedule.keys())
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days)
    ax.set_xticks([x - 0.5 for x in range(1, len(days))], minor=True)
    ax.invert_yaxis()  

    for i, (day, activities) in enumerate(schedule.items()):
        for start, end, activity in activities:
            start_time = datetime.strptime(start, '%H:%M')
            end_time = datetime.strptime(end, '%H:%M')
            duration = end_time - start_time
            if activity.endswith('*'):
                color = 'coral'  
            if activity.endswith('$'):
                color = 'thistle'  
            elif activity == 'work':
                color = 'lightblue'  
            elif activity == 'free time':
                color = 'orchid'  
            elif activity == 'gym':
                color = 'gold'  
            else:
                color = random.choice(['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightsteelblue', 'lightpink'])
            rect = plt.Rectangle((i - 1.0 / 2, start_time.hour + start_time.minute / 60), 1.0, duration.seconds / 3600, color=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(i, start_time.hour + start_time.minute / 60 + duration.seconds / 7200, activity, ha='center')

    ax.set_ylabel('')
    ax.set_title('weekly schedule',y=-0.08)
    ax.xaxis.tick_top()
    plt.grid(axis='x', linestyle='--', linewidth=0.7, color='gray', which='minor')  
    plt.ylim(24, 0)
    plt.grid(False)
    ax.autoscale(enable=True, axis='both', tight=True)
    ax.use_sticky_edges = False
    plt.show()


def plot_schedule2():
    schedule = parse_schedule(SCH_TXT)
    days = list(schedule.keys())
    
    for i, day in enumerate(days):
        fig, ax = plt.subplots(figsize=(10, 6))
        activities = schedule[day]
        activity_list = [activity[2] for activity in activities]
        activity_durations = [(datetime.strptime(activity[1], '%H:%M') - datetime.strptime(activity[0], '%H:%M')).seconds / 3600 for activity in activities]
        
        # Assigning colors based on activity names
        color_map = {}
        color_index = 0
        for activity in activity_list:
            if activity.endswith('*'):
                color_map[activity] = 'coral'
            elif activity == 'work':
                color_map[activity] = 'lightblue'
            elif activity == 'free time':
                color_map[activity] = 'orchid' 
            elif activity.endswith('$'):
                color_map[activity] = 'thistle'  
            elif activity == 'gym':
                color_map[activity] = 'gold' 
            else:
                if activity not in color_map:
                    color_map[activity] = plt.cm.tab10(color_index)
                    color_index += 1
        
        colors = [color_map[activity] for activity in activity_list]
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(activity_durations, labels=activity_list, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(f'Schedule for {day}', pad=20)
        
        # Adding hours to legend
        hours_text = [f'{activity_durations[i]:.2f} hours - {activity_list[i]}' for i in range(len(activity_list))]
        ax.legend(wedges, hours_text, loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Adjusting layout to make room for legend
        plt.subplots_adjust(left=0.1, right=0.7)
        
        # Display the plot
        plt.show()

 
def schedleft(lastl=False):
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    print(f"\n\n{colors.space*2}{schedule_lines[0]}")
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    activities_found = False  
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if current_time <= end_time:
            activities_found = True 
            if line.endswith('*'):
                print(f"{colors.space*2}{colors.WPURPLE}{line}{colors.RESET}") 
            elif line.endswith('course studies'):
                print(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('$'):
                print(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}") 
            elif line.endswith('free'):
                print(f"{colors.space*2}{colors.YELLOW}{line}{colors.RESET}") 
            else:
                print(f"{colors.space*2}{colors.BLUE}{line}{colors.RESET}") 

    if not activities_found:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")

    input(f"\n\n{colors.space*3}{colors.YELLOW}Press any key to continue...{colors.RESET}")

def select_task_from_jobs():
    clear_terminal()
    with open(JOB_TXT, 'r') as file:
        tasks = file.readlines()

    graph = {}
    for task in tasks:
        nodes = task.strip().split(' - ')
        current_node = graph
        for node in nodes:
            if node not in current_node:
                current_node[node] = {}
            current_node = current_node[node]

    print("\n"+colors.WPURPLE+"Available tasks:")
    print(json.dumps(graph, indent=4)) 
    selected_task = input(f"{colors.YELLOW}Enter the new task (q to cancel): {colors.RESET}")
    if selected_task == "q":
        clear_terminal()
        return
    try:
        with open(JobDB, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'tasks': []}

    data['tasks'].append(selected_task)
    with open(JobDB, 'w') as file:
        json.dump(data, file)
    clear_terminal()
    print(f"Task '{selected_task}' saved in JobDB.")


def swap_tasks_in_jobdb():
    clear_terminal()
    with open(JobDB, 'r') as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            print(f"{colors.RED}JobDB not found. Please create tasks first.{colors.RESET}")
            return
    tasks = data.get('tasks', [])
    print(f"\n{colors.YELLOW}Current tasks in JobDB:{colors.RESET}")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.CYAN}{idx}. {task}{colors.RESET}")

    while True:
        try:
            task_index1 = input(f"\nEnter the index of the first task to swap(q):")
            if task_index1 == "q":
                break
            task_index2 = input(f"Enter the index of the second task to swap(q):")
            if task_index2 == "q":
                break
            task_index1 = int(task_index1)
            task_index2 = int(task_index2)
            if 1 <= task_index1 <= len(tasks) and 1 <= task_index2 <= len(tasks):
                tasks[task_index1 - 1], tasks[task_index2 - 1] = tasks[task_index2 - 1], tasks[task_index1 - 1]
                data['tasks'] = tasks

                with open(JobDB, 'w') as file:
                    json.dump(data, file)
                clear_terminal()
                print(f"Tasks at positions {task_index1} and {task_index2} swapped successfully.")
                break
            else:
                clear_terminal()
                print(f"{colors.RED}Invalid task indices. Please enter valid indices.{colors.RESET}")
        except ValueError:
            clear_terminal()
            print(f"{colors.RED}Invalid input. Please enter valid numbers.{colors.RESET}")

def remove_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    tasks = data['tasks']

    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.YELLOW}{idx}. {task}{colors.RESET}")

    index = int(input("\n\nEnter index of tracker to remove: "))
    try:
        tasks.pop(index-1)
        with open(JobDB, 'w') as file:
            json.dump(data, file)
        print("task removed successfully.")
    except IndexError:
        print("Invalid index.")

    


def show_and_mark_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    
    tasks = data['tasks']
    tags_data = load_tags()

    with open(JOB_TXT, 'r') as file:
        words = file.readlines()

    words = [word.strip().split(' - ') for word in words]

    
    if not tasks:
        print(f"{colors.YELLOW}No tasks saved in JobDB.{colors.RESET}")
        return
    
    print(f"{colors.CYAN}Tasks saved in JobDB:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.YELLOW}{idx}. {task}{colors.RESET}")

    while True:
        try:
            task_index = int(input(f"\n{colors.WWITE}Select a task number to mark as done (0 to cancel): {colors.RESET}"))
            if task_index == 0:
                clear_terminal()
                break
            elif 1 <= task_index <= len(tasks):
                selected_task = tasks[task_index - 1]
                print(f"{colors.YELLOW}You selected task: {selected_task}")
                mark_as_done = input(f"{colors.WPURPLE}Have you done this task? (yes/no): {colors.RESET}").lower()
                if mark_as_done == 'yes':
                    mark_as_done_task(str(selected_task))
                    time_taken = input(f"{colors.WPURPLE}How many minutes did it take you to finish the task? {colors.RESET}")
                    show_tags()
                    try:
                        sorted_tags = sorted(tags_data["tags"], key=lambda x: x["name"])
                        tag_number = int(input(f"{colors.WPURPLE}Enter a tag number for the task: {colors.RESET}"))
                        if 1 <= tag_number <= len(sorted_tags):
                            selected_tag = sorted_tags[tag_number - 1]
                            #print(f"{colors.GREEN}Selected Tag: {selected_tag}{colors.RESET}")
                        else:
                            print(f"{colors.RED}Invalid tag number. Please try again.{colors.RESET}")
                    except ValueError:
                        print(f"{colors.RED}Invalid input. Please enter a valid number.{colors.RESET}")
                    try:
                        time_taken = int(time_taken)
                    except ValueError:
                        print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")
                        continue
                        
                    selection = input(f"{colors.WPURPLE}Is this task trackable?{colors.RESET} (yes/no): ")
                    if selection.lower() == 'yes':
                        print("\nSelect the planner to add the task:")
                        print("1. Estimation Planner")
                        print("2. Book Planner")
                        print("3. Lecture Planner")
                        print("4. exercise Planner")
                        print("5. Free Planner")
                        print("6. Goal Planner")

                        try:
                            planner_index = int(input("Enter the index of the planner: "))
                            if 1 <= planner_index <= 6:
                                planner_functions = [estimation.add_task, bookplanner.add_task, lectureplanner.add_task,
                                                    xestimation.add_task, freeplanner.add_task, goalplanner.add_task]

                                selected_planner = planner_functions[planner_index - 1]
                                selected_planner(minutes=time_taken,strn=selected_task)
                            else:
                                print(f"{colors.RED}Invalid planner index. Please try again.{colors.RESET}")
                        except ValueError:
                            print(f"{colors.RED}Invalid input. Please enter a valid number.{colors.RESET}")
                    
                    reminderfile = input(f"{colors.WPURPLE}Do you want to set a reminder?{colors.RESET} (yes/no): ")
                    if reminderfile.lower() in ['yes', 'y']:
                        reminder.add_reminder(selected_task=selected_task)

                    if time_taken>0:
                        completed_task = {
                            "task": selected_task,
                            "time_taken": time_taken,
                            "completed_at": datetime.now().strftime('%Y-%m-%d'),
                            "tag": selected_tag['name']
                        }

                        if not os.path.exists(TIMEJC):
                            with open(TIMEJC, 'w') as time_file:
                                json.dump([completed_task], time_file, indent=4)
                        else:
                            with open(TIMEJC, 'r+') as time_file:
                                time_data = json.load(time_file)
                                time_data.append(completed_task)
                                time_file.seek(0)
                                json.dump(time_data, time_file, indent=4)
                    
                    matching_word = None
                    for word in words:
                        if selected_task in word:
                            matching_word = word
                            break

                    if matching_word:
                        if selected_task == matching_word[-1]:
                            pass
                        else:
                            print(f"{colors.WPURPLE}The selected task matches a word in your list: {matching_word}{colors.RESET}")
                            replace_task = input(f"{colors.WPURPLE}Do you want to replace it with the next word? (yes/no): {colors.RESET}").lower()
                            if replace_task == 'yes':
                                replace_index = matching_word.index(selected_task)
                                next_word_index = (replace_index + 1) % len(matching_word)
                                selected_task = matching_word[next_word_index]
                                clear_terminal()
                                print(f"\n\nTask replaced with: {selected_task}")

                                tasks[task_index - 1] = selected_task
                                data['tasks'] = tasks

                                with open(JobDB, 'w') as file:
                                    json.dump(data, file, indent=4)
                                break



                    tasks.pop(task_index - 1)
                    clear_terminal()  
                    print(f"\n\nTask '{selected_task}' removed from JobDB.")
                with open(JobDB, 'w') as file:
                    json.dump(data, file)
            else:
                print(f"Task '{selected_task}' not marked as done.")
            break
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")


def print_first_entry_from_json():
    line = show_schedule_by_time(print_output=False)
    if line == True:
       show_schedule_by_time(print_output=True)
    else:
        try:
            with open(JobDB, 'r') as file:
                data = json.load(file)
                tasks = data.get('tasks', [])
                if tasks:
                    first_entry = tasks[0]
                    print(f"{colors.space*7}{colors.WPURPLE}Active task: {first_entry}/{personalplanner.get_top_task()}{colors.RESET}")
                else:
                    print(f"{colors.space*7}{colors.BLUE}JobDB is empty")
        except FileNotFoundError:
            print(f"{colors.RED}{colors.space*7}JobDB not found. Please create tasks first.{colors.RESET}")


def view_statistics():
    clear_terminal()

    try:
        with open(TIMEJC, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{colors.RED}No data available in TIMEJC. Please complete tasks first.{colors.RESET}")
        input("\n\nPress any key to continue...")
        clear_terminal()
        return

    total_time = 0
    task_count = len(data)
    tracker_time = {}

    for task in data:
        time_taken = int(task["time_taken"])
        total_time += time_taken

        task_name = task["task"]
        if task_name in tracker_time:
            tracker_time[task_name] += time_taken
        else:
            tracker_time[task_name] = time_taken

    avg_time = total_time / task_count if task_count > 0 else 0

    clear_terminal()
    print(f"\n\nTotal time spent on completed tasks: {total_time} minutes / {total_time / 60:.2f} hours")
    print(f"Average time spent on tasks: {avg_time:.2f} minutes / {avg_time / 60:.2f} hours")
    if tracker_time:
        print("\n\n----------------------")
        print("Top 5 completed tasks:")
        print("----------------------")
        sorted_tasks = sorted(tracker_time, key=tracker_time.get, reverse=True)
        for i, task_name in enumerate(sorted_tasks[:5]):
            if tracker_time[task_name] < 60:
                print(f"{i + 1}. {task_name}: {tracker_time[task_name]} minutes")
            else:
                print(f"{i + 1}. {task_name}: {tracker_time[task_name] / 60:.2f} hours")

    input("\n\nPress any key to continue...")
    clear_terminal()

def mark_as_done_task(task_name):
    try:
        with open(EBDB, 'r') as file:
            endeavors_data = json.load(file)
    except FileNotFoundError:
        return

    for endeavor in endeavors_data:
        if endeavor.get("name") == task_name:
            endeavor["done"] = True
            break

    with open(EBDB, 'w') as file:
        json.dump(endeavors_data, file, indent=4)


def calculate_and_print_free_hours():
    workperday = estimation.tracker_greedy(rint=False)
    bookperday = bookplanner.tracker_greedy(rint=False)
    exerperday = xestimation.tracker_greedy(rint=False)
    lectperday = lectureplanner.tracker_greedy(rint=False)
    total_tag = float(show_tags(showl=True))
    free_activities_hours = {day_name: 0 for day_name in day_names.values()}  
    project_activities_hours = {day_name: 0 for day_name in day_names.values()}  
    project_activities_vods = {day_name: 0 for day_name in day_names.values()}
    project_activities_ex = {day_name: 0 for day_name in day_names.values()} 

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    current_day_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('#') and line[2:] in day_names.values():
            current_day_name = line[2:]
        elif current_day_name and line:
            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free time":
                free_activities_hours[current_day_name] += activity_hours
                project_activities_ex[current_day_name] += activity_hours
                project_activities_vods[current_day_name] += activity_hours
            elif activity.strip() == "work":
                project_activities_hours[current_day_name] += activity_hours

    print(f"\n\n{colors.YELLOW}{colors.space*13}||Total Free Hours for Each Day||{colors.RESET}")
    print(f"{colors.YELLOW}{colors.space*3}{colors.line2*86}{colors.RESET}")
    total_sum_free = 0
    total_sum_project = 0
    total_sum_vods = 0
    total_sum_exercise = 0
    for day, total_hours in free_activities_hours.items():
        total_sum_free += total_hours
    for day, total_hours_project in project_activities_hours.items():
        total_sum_project += total_hours_project
    for day, total_hours_vods in project_activities_vods.items():
        total_sum_vods += total_hours_vods
    for day, total_hours_ex in project_activities_ex.items():
        total_sum_exercise += total_hours_ex

    workamount_free = workperday*7/total_sum_free
    bookamount_free = bookperday*7/total_sum_free
    exerciseam_free = exerperday*7/total_sum_free
    lecturetim_free = lectperday*7/total_sum_free
    work_hour = 50*total_sum_free/60
    for day, total_hours in free_activities_hours.items():
        total_hours_project = project_activities_hours.get(day, 0)
        total_hours_vods = project_activities_vods.get(day, 0) 
        total_hours_ex = project_activities_ex.get(day, 0)
        print(colors.space*3+colors.YELLOW+"|{:<5}-{:<17}|{:<20}|{:<20}|{:<20}|{:<21}|{:<10}|{:<10}|".format(f"{day}",
                                                                                                      f" {total_hours:.2f} hours{colors.YELLOW}",
                                                                                                      f"{colors.GREEN}(TW:{workamount_free*total_hours:.2f}){colors.YELLOW}",
                                                                                                      f"{colors.CYAN}(TB:{bookamount_free*total_hours:.2f}){colors.YELLOW}",
                                                                                                      f"{colors.CYAN}(TT:{exerciseam_free*total_hours_ex:.2f}){colors.YELLOW}",
                                                                                                      f"{colors.CYAN}(TV:{lecturetim_free*total_hours/60:.2f}h){colors.YELLOW}",
                                                                                                      f"{colors.WPURPLE}(W:{total_hours_project:.2f}){colors.YELLOW}",
                                                                                                      f"{colors.LBLUE}(TPD:{total_tag/total_sum_free*total_hours:.2f}){colors.YELLOW}"
                                                                                                      ))
    print(f"{colors.YELLOW}{colors.space*3}{colors.line2*86}{colors.RESET}")
    print(colors.YELLOW+colors.space*10+"|{:<10}|{:<10}|{:<10}|".format(f" free time: {total_sum_free:.2f} ",
                                                                        f" work hour: {total_sum_project:.2f} ",
                                                                        f" study&etc hour: {work_hour+total_sum_project:.2f} "))

    print(f"\n{colors.GREEN}{colors.space*2}work per average:{colors.WPURPLE} ({workperday:.2f} and week is {workperday*7:.2f})")
    print(f"{colors.CYAN}{colors.space*2}work per hour is: {workamount_free:.2f} which is {colors.RED}{workamount_free*60:.2f} minutes")
    print(f"{colors.GREEN}{colors.space*2}book per average:{colors.WPURPLE} ({bookperday:.2f} and week is {bookperday*7:.2f})")
    print(f"{colors.CYAN}{colors.space*2}book per hour is: {bookamount_free:.2f} which is {colors.RED}{bookamount_free*7:.2f} minutes")
    print(f"{colors.GREEN}{colors.space*2}lecture total is:{colors.WPURPLE} {lectperday*7/60:.2f} hours which is {colors.RED}{lectperday:.2f} minutes per day")

    return total_sum_free



def sum_and_print_activities():
    activity_sums = {
        "Free": 0,
        "work": 0,
        "Classes": 0,
        "course studies": 0,
        "Assigned tasks": {},
        "Other stuff": {}
    }

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.endswith('$'):
            start_time, end_time, task = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if task in activity_sums["Assigned tasks"]:
                activity_sums["Assigned tasks"][task] += activity_hours
            else:
                activity_sums["Assigned tasks"][task] = activity_hours
        elif line.endswith('*'):
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["Classes"] += activity_hours
        elif "course studies" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["course studies"] += activity_hours
        elif "free time" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["Free"] += activity_hours
        elif "work" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["work"] += activity_hours
        else:
            if len(line.split(' - ')) == 3:
                start_time, end_time, activity_name = line.split(' - ')
                activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
                # Store other activities in the dictionary
                if activity_name in activity_sums["Other stuff"]:
                    activity_sums["Other stuff"][activity_name] += activity_hours
                else:
                    activity_sums["Other stuff"][activity_name] = activity_hours

    print(f"\n{colors.CYAN}{colors.space*2}Activity Sums for the Week:")
    for activity, total_hours in sorted(activity_sums.items(), key=lambda x: sum(x[1].values()) if isinstance(x[1], dict) else x[1], reverse=True):
        if activity == "Assigned tasks" or activity == "Other stuff":
            total_assigned_hours = sum(total_hours.values())
            print(f"{colors.space*3}{activity}: {total_assigned_hours:.2f} hours{{")
            for task, hours in sorted(total_hours.items(), key=lambda x: x[1], reverse=True):
                print(f"{colors.CYAN}{colors.space*7}{task}: {hours:.2f} hours {colors.RESET}")
            print(f"{colors.space*5}}}")
        else:
            print(f"{colors.space*3}{activity}: {total_hours:.2f} hours")

def show_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    
    tasks = data['tasks']

    with open(JOB_TXT, 'r') as file:
        words = file.readlines()

    words = [word.strip().split(' - ') for word in words]

    
    if not tasks:
        print(f"{colors.YELLOW}No tasks saved in JobDB.{colors.RESET}")
        return
    
    print(f"\n\n{colors.space*7}{colors.CYAN}Current Active Tasks in JobDB")
    print(f"{colors.space*7}{colors.CYAN}{colors.line2*50}")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.space*8}{colors.GREEN}{idx}.{colors.YELLOW} {task}{colors.RESET}")

def show_schedule_py():
    activities_found = None
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if start_time <= current_time <= end_time:
            if activity != "free time":
                activities_found = line
            else:
                activities_found = str(show_schedule_py())
            print(f"{colors.space*7}{colors.CYAN}got scheduled activity: {colors.WPURPLE}{activities_found}{colors.RESET}") 
    if activities_found is None:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")
    return activities_found



def calculate_work(select):
    if select == 'work':
        workperday = estimation.tracker_greedy(rint=False)
    elif select == 'videos':
        workperday = lectureplanner.tracker_greedy(rint=False)
    elif select == 'book':
        workperday = bookplanner.tracker_greedy(rint=False)
    free_activities_hours = {day_name: 0 for day_name in day_names.values()}  
    project_activities_hours = {day_name: 0 for day_name in day_names.values()}  

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    current_day_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('#') and line[2:] in day_names.values():
            current_day_name = line[2:]
        elif current_day_name and line:
            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free time":
                free_activities_hours[current_day_name] += activity_hours
            elif activity.strip() == "work":
                project_activities_hours[current_day_name] += activity_hours

    total_sum_free = 0
    for day, total_hours in free_activities_hours.items():
        total_sum_free += total_hours
    workamount = workperday*7/total_sum_free
   
    return workamount



def empty_tmpbox():
    data = {'boxes': []}
    with open(TMPBOX, 'w') as file:
        json.dump(data, file)

def todaysboxes(addrem):
    get_schedule_output(lastl=True)
    global total_hours
    try:
        with open(TMPBOX, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'boxes': []}
    
    total_boxes = math.ceil(float(total_hours) / 1.25)
    # if len(data['boxes']) <= total_boxes:
    #     pass
    # else:
    #     total_boxes = len(data['boxes'])

    screen_chart = [[' ' for _ in range(50)] for _ in range(total_boxes)]
    while True:
        print(f"\n\n{colors.CYAN}Today's Boxes: {total_boxes}")
        if len(data['boxes']) <= total_boxes:
            pass
        else:
            total_boxes = len(data['boxes'])
        print(f"{colors.YELLOW}{'-' * 50}")
        
        for idx in range(total_boxes):
            if idx < len(data['boxes']):
                box_text = data['boxes'][idx]
                print(f"{colors.YELLOW}|{box_text.center(48)}|")
            else:
                print(f"{colors.YELLOW}|{' ' * 48}|")
            print(f"{colors.YELLOW}{'-' * 50}")
        if addrem==True:
            action = input(f"\n{colors.WWITE}Do you want to add or remove a box? (a/r/q): {colors.RESET}").lower()

            if action == 'a':
                if len(data['boxes']) < total_boxes:
                    text = input(f"{colors.YELLOW}Enter text for the box: {colors.RESET}")
                    box_index = len(data['boxes'])
                    data['boxes'].append(text)
                    row = box_index
                    col = 2  # Adjust the starting column based on your design
                    screen_chart[row][col:col + len(text)] = text
                    clear_terminal()
                    print(f"{colors.GREEN}Box added successfully.{colors.RESET}")
                else:
                    clear_terminal()
                    print(f"{colors.RED}All boxes are already filled. Cannot add more boxes.{colors.RESET}")
                    overwrite = input("Do you want to overwrite the box number?(y/n)")
                    if overwrite == "y":
                        clear_terminal()
                        total_boxes =+ 1
                        text = input(f"{colors.YELLOW}\nEnter text for the box: {colors.RESET}")
                        box_index = len(data['boxes'])+1
                        data['boxes'].append(text)
                        row = box_index
                        col = 2 
                        clear_terminal()
                        print(f"{colors.GREEN}Box added successfully.{colors.RESET}")
                    else:
                        pass

            elif action == 'r':
                print(f"\n{colors.YELLOW}Boxes:")
                for idx, box_text in enumerate(data['boxes']):
                    print(f"{colors.YELLOW}{idx + 1}. {box_text}")
                try:
                    remove_index = int(input(f"{colors.YELLOW}Enter the index of the box to remove: {colors.RESET}")) - 1
                    if 0 <= remove_index < len(data['boxes']):
                        removed_text = data['boxes'].pop(remove_index)
                        clear_terminal()
                        print(f"{colors.GREEN}Box '{removed_text}' removed successfully.{colors.RESET}")
                        # Update the screen chart when removing a box
                        screen_chart[remove_index][2:2 + len(removed_text)] = [' '] * len(removed_text)
                    else:
                        clear_terminal()
                        print(f"{colors.RED}Invalid box index.{colors.RESET}")
                except ValueError:
                    clear_terminal()
                    print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")

            elif action == 'q':
                with open(TMPBOX, 'w') as file:
                    json.dump(data, file)
                break

            else:
                clear_terminal()
                print(f"{colors.RED}Invalid action. Please enter 'a', 'r', or 'q'.{colors.RESET}")
        else:
            break

def generate_recent_days_histogram():
    try:
        with open(TIMEJC, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{colors.RED}No data available in TIMEJC. Please complete tasks first.{colors.RESET}")
        return

    recent_days = [datetime.now() - timedelta(days=i) for i in range(11, -1, -1)]
    recent_days_str = [day.strftime('%Y-%m-%d') for day in recent_days]

    task_colors = {}  # To store colors for each task

    # Initialize data for each day
    day_data = {day_str: {} for day_str in recent_days_str}

    for task in data:
        task_name = task["task"]
        time_taken = task["time_taken"]
        completed_at = datetime.strptime(task["completed_at"], '%Y-%m-%d')
        completed_at_str = completed_at.strftime('%Y-%m-%d')

        # Initialize task color if not already assigned
        if task_name not in task_colors:
            task_colors[task_name] = np.random.rand(3,)

        # Add task time to the corresponding day
        if completed_at_str in day_data:
            if task_name in day_data[completed_at_str]:
                day_data[completed_at_str][task_name] += time_taken
            else:
                day_data[completed_at_str][task_name] = time_taken

    # Sort legend by total minutes spent on each task
    sorted_legend = sorted(task_colors.keys(), key=lambda x: sum(day_data[day_str].get(x, 0) for day_str in recent_days_str), reverse=True)

    # Create a stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(recent_days_str))

    for task_name in sorted_legend[:25]:  # Limit to the top 25 tasks
        color = task_colors[task_name]
        task_hours = [day_data[day_str].get(task_name, 0) / 60 for day_str in recent_days_str]
        ax.bar(recent_days, task_hours, label=task_name, color=color, alpha=0.7, edgecolor='black', bottom=bottom)
        bottom += task_hours  # Update the bottom position for the next task

    ax.set_title('Recent 12 Days Activities')
    ax.set_xlabel('Days')
    ax.set_ylabel('Minutes')
    ax.legend()
    ax.xaxis_date()  # Treat x-axis as dates

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def load_tags():
    try:
        with open(TAGS_FILE, 'r') as file:
            tags_data = json.load(file)
    except FileNotFoundError:
        tags_data = {"tags": []}
    return tags_data

def save_tags(tags_data):
    with open(TAGS_FILE, 'w') as file:
        json.dump(tags_data, file, indent=4)


def show_tags(showl=False,sortlist=False):
    tags_data = load_tags()
    tag_sum = 0
    if sortlist:
        sorted_tags = sorted(tags_data["tags"], key=lambda x: float(x["time"]), reverse=True)  
    else:
        sorted_tags = sorted(tags_data["tags"], key=lambda x: x["name"]) 
    if not showl:
        print(f"\n{colors.YELLOW}Existing tags:{colors.RESET}")
    for idx, tag in enumerate(sorted_tags, start=1):
        tag_name = tag["name"]
        tag_time = tag["time"]
        tag_sum += float(tag_time)
        if not showl:
            print(f"{colors.PURPLE}{idx}.{colors.LBLUE} {tag_name} {colors.CYAN}- {tag_time} hours{colors.RESET}")
    if not showl:
        print(f"{colors.BLUE}tag sum hour is: {tag_sum:.2f} hours{colors.RESET}")
    if showl == True:
        return tag_sum





def manage_tags():
    clear_terminal()

    while True:
        tags_data = load_tags()
        print(f"\n{colors.YELLOW}Tag Management Menu:")
        print(f"{colors.CYAN}a. add a new tag{colors.RESET}")
        print(f"{colors.CYAN}m. Modify an existing tag{colors.RESET}")
        print(f"{colors.CYAN}s. show tags{colors.RESET}")
        print(f"{colors.CYAN}r. Remove a tag{colors.RESET}")
        print(f"{colors.CYAN}q. Exit{colors.RESET}")

        choice = input(f"\n{colors.PURPLE}Enter your choice{colors.RESET}: ")
        
        if choice == "a":
            new_tag = input("Enter the name of the new tag: ")
            time = input("Enter the hour Amount: ")
            tags_data["tags"].append({"name": new_tag, "time": time})
            clear_terminal()
            print(f"Tag '{new_tag}' created successfully with {time} hours.")
            save_tags(tags_data)
        elif choice == "s":
            clear_terminal()
            show_tags(sortlist=True)
            input(f"\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "m":
            clear_terminal()
            print(f"\n{colors.YELLOW}Existing tags:{colors.RESET}")
            for idx, tag in enumerate(tags_data["tags"], start=1):
                print(f"{colors.PURPLE}{idx}.{colors.LBLUE} {tag['name']} {colors.CYAN}- {tag['time']} hours{colors.RESET}")
            try:
                edit_index = int(input("Enter the index of the tag to edit: ")) - 1
                if 0 <= edit_index < len(tags_data["tags"]):
                    edited_tag_time = input("Enter the new hour amount for the tag: ")
                    if float(edited_tag_time) != 0:
                        tags_data["tags"][edit_index]["time"] = edited_tag_time
                        clear_terminal()
                        print(f"Tag edited successfully.")
                        save_tags(tags_data)
                    else:
                        clear_terminal()
                else:
                    clear_terminal()
                    print("Invalid tag index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "r":
            clear_terminal()
            print(f"\n{colors.YELLOW}Existing tags:{colors.RESET}")
            for idx, tag in enumerate(tags_data["tags"], start=1):
                print(f"{colors.PURPLE}{idx}.{colors.LBLUE} {tag['name']} {colors.CYAN}- {tag['time']} hours{colors.RESET}")
            try:
                remove_index = int(input("Enter the index of the tag to remove: ")) - 1
                if 0 <= remove_index < len(tags_data["tags"]):
                    removed_tag = tags_data["tags"].pop(remove_index)
                    clear_terminal()
                    print(f"Tag '{removed_tag}' removed successfully.")
                    save_tags(tags_data)
                else:
                    clear_terminal()
                    print("Invalid tag index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")

def generate_recent_days_histogram2():
    try:
        with open(TIMEJC, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{colors.RED}No data available in TIMEJC. Please complete tasks first.{colors.RESET}")
        return

    # Load tags data
    tags_data = load_tags()
    tags_data2 = tags_data["tags"]
    tags = [tag["name"] for tag in tags_data2]


    recent_days = [datetime.now() - timedelta(days=i) for i in range(6, -1, -1)]  # Current week
    recent_days_str = [day.strftime('%Y-%m-%d') for day in recent_days]

    task_hours_by_tag = {tag: [0] * len(recent_days) for tag in tags}

    for task in data:
        task_name = task["task"]
        time_taken = task["time_taken"]
        completed_at = datetime.strptime(task["completed_at"], '%Y-%m-%d')
        completed_at_str = completed_at.strftime('%Y-%m-%d')

        # Check if the task has a tag
        tag = next((task.get("tag") for task in data if task.get("task") == task_name), None)
        # Add task time to the corresponding day and tag
        if completed_at_str in recent_days_str and tag in tags:
            day_index = recent_days_str.index(completed_at_str)
            task_hours_by_tag[tag][day_index] += time_taken

    # Create a stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))

    bottom = np.zeros(len(recent_days))

    for tag in tags:
        color = np.random.rand(3,)
        task_hours = task_hours_by_tag[tag]
        ax.bar(recent_days, task_hours, label=tag, color=color, alpha=0.7, edgecolor='black', bottom=bottom)
        bottom += task_hours

    ax.set_title('Recent Week Tasks Distribution by Tag')
    ax.set_xlabel('Days')
    ax.set_ylabel('Hours')
    ax.legend()
    ax.xaxis_date()  # Treat x-axis as dates

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def load_seven_days():
    try:
        with open(SEVEN_DAYS_FILE, 'r') as file:
            seven_days_data = json.load(file)
    except FileNotFoundError:
        seven_days_data = {"date": datetime.now().strftime('%Y-%m-%d')}
        save_seven_days(seven_days_data)
    return seven_days_data

def save_seven_days(seven_days_data):
    with open(SEVEN_DAYS_FILE, 'w') as file:
        json.dump(seven_days_data, file, indent=4)

def save_today_date():
    seven_days_data = load_seven_days()
    current_date = datetime.now().strftime('%Y-%m-%d')

    print((datetime.strptime(current_date, '%Y-%m-%d') - datetime.strptime(seven_days_data["date"], '%Y-%m-%d')).days)

    
    if "date" not in seven_days_data or (datetime.strptime(current_date, '%Y-%m-%d') - datetime.strptime(seven_days_data["date"], '%Y-%m-%d')).days > 7:
        seven_days_data["date"] = current_date
        save_seven_days(seven_days_data)

def load_tasks_data():
    try:
        with open(TIMEJC, 'r') as file:
            tasks_data = json.load(file)
    except FileNotFoundError:
        tasks_data = []
    return tasks_data

def sum_and_show_tag_percentages():
    seven_days_data = load_seven_days()
    current_date = datetime.now().strftime('%Y-%m-%d')
    days_difference = (datetime.strptime(current_date, '%Y-%m-%d') - datetime.strptime(seven_days_data['date'], '%Y-%m-%d')).days

    if "date" not in seven_days_data or days_difference <= 7:
        # Proceed with summing tasks and calculating percentages
        with open(TIMEJC, 'r') as file:
            tasks_data = json.load(file)

        tags_data = load_tags()

        tag_sums = {tag["name"]: 0 for tag in tags_data["tags"]}
        tag_total_times = {tag["name"]: float(tag["time"]) for tag in tags_data["tags"]}

        for task in tasks_data:
            task_date = task.get("completed_at", "")
            task_time_taken = task.get("time_taken", 0)
            task_tag = task.get("tag", "")

            # Only consider tasks from today and the date saved in SEVEN_DAYS_FILE
            if seven_days_data["date"] <= task_date <= current_date:
                if task_date and task_time_taken and task_tag in tag_sums:
                    tag_sums[task_tag] += task_time_taken

        print(f"\n{colors.CYAN}{colors.space*35}||| Tag Percentages for Today and the Last 7 Days |||")
        print(colors.CYAN+"-" * (129)+colors.RESET)

        max_tag_length = max(len(tag_name) for tag_name in tag_sums.keys())
        sorted_tags = sorted(tag_sums.items(), key=lambda x: (x[1] / tag_total_times[x[0]]) * 100)


        for tag_name, tag_sum in sorted_tags:
                    total_time = tag_total_times.get(tag_name, 0)
                    if total_time < 0.15:
                            continue
                    if total_time > 0:
                        hours_done = tag_sum / 60  # Convert to hours
                        hours_left = total_time - hours_done
                        percentage = (hours_done / total_time) * 100

                        # Create vertical bars
                        done_bar = int(percentage)
                        left_bar = 100 - done_bar

                        tag_padding = ' ' * (max_tag_length - len(tag_name))
                        if percentage < 25:
                            percentage_color = colors.RED
                        elif percentage < 60:
                            percentage_color = colors.BLUE
                        elif percentage <= 99:
                            percentage_color = colors.GREEN
                        elif percentage < 110:
                            percentage_color = colors.YELLOW
                        elif percentage > 110:
                            percentage_color = colors.RED
                        print(f"{colors.YELLOW}- {tag_name}:{tag_padding} {colors.RESET}{percentage_color}[{'=' * done_bar}{' ' * left_bar}] {percentage:.2f}%{colors.RESET}")
                        print(f"{colors.PURPLE}  ({hours_done:.2f} hours done/{total_time:.2f} hours total) | {hours_left:.2f} hours left {colors.RESET}")
                        print(colors.CYAN+"-" * (129)+colors.RESET)
                    else:
                        tag_padding = ' ' * (max_tag_length - len(tag_name))
                        print(f"{colors.YELLOW}- {tag_name}:{tag_padding} No tasks recorded{colors.RESET}")

        print(f"{colors.BLUE}{colors.space*43}<< {colors.WWITE}{7-days_difference} days are left within the week{colors.BLUE} >>{colors.RESET}")
    else:
        print(f"\n{colors.YELLOW}Data for today and the last 7 days is not available. Please complete tasks first.{colors.RESET}")


def main():
    clear_terminal()
    save_today_date()

    while True:
        print("\n\n")
        print_first_entry_from_json()
        print(f"\n{colors.YELLOW}||Schedule Program||{colors.RESET}\n")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Change Schedules{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Schedules{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Show Tody's left schedule{colors.RESET}")
        print(f"{colors.CYAN}p.{colors.RESET} {colors.YELLOW}Show Chart{colors.RESET}")
        print(f"{colors.CYAN}pp.{colors.RESET} {colors.YELLOW}Show PieChart{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Show Schedule by Current Time{colors.RESET}")
        print(f"{colors.CYAN}w.{colors.RESET} {colors.YELLOW}Swap places{colors.RESET}")
        print(f"{colors.CYAN}k.{colors.RESET} {colors.YELLOW}Select a task{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Complete a task{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Show statistics{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Print week's free time and activities{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}remove a task{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Manage Tags{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "s":
            clear_terminal()
            print("\n\n"+get_schedule_output(lastl=True))
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "n":
            clear_terminal()
            edit_notes(files=False)
            clear_terminal()
        elif choice == "l":
            clear_terminal()
            schedleft()
            clear_terminal()
        elif choice == "d":
            clear_terminal()
            sum_and_show_tag_percentages()
            resetday = input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...(r to reset){colors.RESET}")
            if resetday == "r":
                seven_days_data = {"date": datetime.now().strftime('%Y-%m-%d')}
                save_seven_days(seven_days_data)
            view_statistics()
            generate_recent_days_histogram()
            generate_recent_days_histogram2()
            clear_terminal()
        elif choice == "t": 
            clear_terminal()
            print("\n\n")
            manage_tags()
            #show_schedule_by_time(print_output=True)
            #input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "r":
            clear_terminal()
            remove_tasks()
            clear_terminal()
        elif choice == "g": 
            clear_terminal()
            print("\n\n")
            sum_and_print_activities()
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "b":
            clear_terminal()
            todaysboxes(addrem=True)
            clear_terminal()
        elif choice == "p":
            clear_terminal()
            plot_schedule()
            clear_terminal()
        elif choice == "pp":
            clear_terminal()
            plot_schedule2()
            clear_terminal()
        elif choice == "k":
            select_task_from_jobs()
        elif choice == "w":
            swap_tasks_in_jobdb()
        elif choice == "f":
            clear_terminal()
            calculate_and_print_free_hours()
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "c":
            clear_terminal()
            show_and_mark_tasks()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()