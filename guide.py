from datetime import datetime, timedelta
import os, json, io, sys, re , progress
from uptils import foldermaker, colors
from uptils.clearterminal import clear_terminal
from estimations import estimation, freeplanner, xestimation, bookplanner, lectureplanner, goalplanner
from modules import (activity, calendar, daycalculator, endeavor,
                     flashcard, newbook, notes, project, tasks,
                     repetition, subjects, weighttracker , videolecture,
                     streaks, schedule, tgbot, personalplanner)

start_file = os.path.join(colors.notes_file, 'start.json')


def telegram_status_print():
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    goalplanner.tracker_greedy(rint=True)
    estimation.tracker_greedy(rint=True)
    xestimation.tracker_greedy(rint=True)
    lectureplanner.tracker_greedy(rint=True)
    freeplanner.tracker_greedy()
    bookplanner.tracker_greedy(rint=True)
    print("#work🏮🎈")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    repetition.show_reminders()
    print("#spaced_repetition #repetition #reminders🕐🕠🕘")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass
    

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    today_index = (datetime.today().weekday() + 2) % 7
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    endeavor.show_endeavors()
    print("#endeavors #routine🌀🧘‍♂️")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    schedule.todaysboxes(addrem=False)
    print("#boxes📦🐍")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    streaks.show_streaks()
    print("#goals #subgoals #streaks🎯⭐️")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    tasks.taskfile(show=False)
    print("#tasks #deadline ⚠️⚠️")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    current_date = datetime.now().strftime('%d-%m-%Y')
    calendar.display_calendar(current_date,printtrue=False)
    print("#calendar 🗓📅")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    schedule.show_tasks()
    print("#tasks #jobdb 📔🎸")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
    except:
        pass
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    schedule.sum_and_show_tag_percentages()
    print("#work #hours ⏰ 🕒 ")
    function_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    function_output_cleaned = ansi_escape.sub('', function_output)
    try:
        tgbot.pytelbot(function_output_cleaned)
        tgbot.pytelbot("Have a Great day✨🕊🙏🏻")
    except:
        pass

def main():
    try:
        tgbot.check_and_update_json()
    except:
        pass
    activity.check_work_finished()
    start_time = None
    if os.path.exists(start_file):
        with open(start_file, "r") as file:
            start_data = json.load(file)
        start_time = datetime.strptime(start_data["start_time"], "%Y-%m-%d %H:%M:%S")
    if start_time:
                if start_time.date() != datetime.now().date():
                    start_time = None
                    os.remove(start_file)
    clear_terminal()

    while True:
        #print("{:+^80}\n".format(""))
        print(colors.WWITE+"\n")
        print(colors.space*9+"{:^80}".format("VISION GUIDE"))
        #print("{:+^84}".format(""))
        print(colors.space*7+colors.plus*42)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" a. activity  - activity log",           " t.  project  - project estimation(t/tfbv)"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" y. streaks   - streak tracker",         " tg. goals    - macro-goal setting"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" d. Endeavor  - daily planner",          " k.  tasks    - kanban board"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" s. schedule  - weekly schedule",        " r.  remind   - spaced repetition"))
        print(colors.space*7+colors.plus+colors.line*19+" "+colors.line*21+colors.plus)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" b. books     - current books repo(n)",  " m. flashcard - language flashcard"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" v. video     - video lecture",          " p. project   - project automation"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" u. subject   - subject selector",       " w. weight    - weight tracker"))
        print(colors.space*7+colors.plus+colors.line*19+" "+colors.line*21+colors.plus)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" c. calendar  - calendar program",       " e. task      - show active task(f)"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" j. date      - change cycle date",      " d. old Endeavor "))
        print(colors.space*7+"‖"+colors.plus*19+"  "+colors.plus*21+"‖")
        print("")
        print(colors.space*7+"{:<50}{:>30}".format(f"{daycalculator.days} days left {daycalculator.tldata()}", f"Today is {daycalculator.weektoday}"))
    
        #print(f"hours in a week is {daycalculator.sum_values}, estimated work is {daycalculator.todayhours} hour and {round(books.pages_per_today)} pages.")


        try:
            if activity.work_finished == False:           
                print()
                schedule.print_first_entry_from_json()
                if start_time:
                    time_elapsed = str(datetime.now() - start_time).split('.')[0]
                    print(f"{colors.space*7}{colors.CYAN}Start Time: {colors.WWITE}{start_time.strftime('%H:%M:%S')}{colors.CYAN} - Elapsed Time: {colors.WWITE}{str(time_elapsed)}{colors.RESET}")
                else:
                    print(f"{colors.space*7}{colors.RED}Start Button{colors.RESET} - {colors.YELLOW}Press [sa] {colors.RESET}{colors.YELLOW}to start the button.{colors.RESET}")
                #activity.calculate_activity_rating()
                activity.check_work_finished()
            else:
                activity.check_work_finished()

            progress.check_trackers()


            print(colors.space*7+colors.cline*15)
            print(colors.space*7+colors.folder+"(tr) trackers"+colors.space*7+colors.folder+"(re) reminders")
            print(colors.space*7+colors.folder+"(ta) tasks"+colors.space*10+colors.folder2+"(sf) streaks")
            print(colors.space*7+colors.folder2+"(sc/fpc) schedule"+colors.space*3+colors.folder2+"(ro) routine")
            print(colors.space*7+colors.folder2+"(nn) notes"+colors.space*10+"🚪"+"(q) quit")
        except:
            print("\n\nERROR: PROCESS UNIDENTIFIED")
        print(f"\n{colors.space*7}time left till end of the day: {daycalculator.hours} hours, {daycalculator.minutes} minutes.")
        select = input(colors.space*7+"what you wanna do(cc to clock out/show/push)?:   ")

        if select == "show":
            clear_terminal()
            print("-"*98)
            schedule.show_schedule_by_time(print_output=True)
            schedule.calculate_and_print_free_hours()
            schedule.schedleft()
            clear_terminal()
            try:
                goalplanner.tracker_greedy(rint=True)
                estimation.tracker_greedy(rint=True)
                xestimation.tracker_greedy(rint=True)
                lectureplanner.tracker_greedy(rint=True)
                freeplanner.tracker_greedy()
                bookplanner.tracker_greedy(rint=True)
            except:
                print("\n\nERROR: PROCESS UNIDENTIFIED")
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
            print("-"*98)
            current_date = datetime.now().strftime('%d-%m-%Y')
            calendar.display_calendar(current_date,printtrue=False)
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
            print("-"*98)
            streaks.show_streaks()
            schedule.show_tasks()
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
            print("-"*98)
            schedule.todaysboxes(addrem=False)
            input(f"{colors.YELLOW}\n\nPress any key to continue...{colors.RESET}")
            clear_terminal()
            print("-"*98)
            endeavor.show_endeavors()
            input(f"{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
            print("-"*98)
            repetition.show_reminders()
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
            tasks.taskfile(show=False)
            input("\n\nPress any key to continue...")
            clear_terminal()
        elif select == "push":
            telegram_status_print()
            clear_terminal()
        elif select == "d":
            clear_terminal()
            personalplanner.main()
        elif select == "dd":
            clear_terminal()
            endeavor.main()
        elif select == "k":
            clear_terminal()
            tasks.main()
        elif select == "teleg":
            clear_terminal()
            tgbot.check_and_update_json()
        elif select == "e":
            clear_terminal()
            schedule.select_task_from_jobs()
            clear_terminal()
        elif select == "fd":
            clear_terminal()
            schedule.show_and_mark_tasks()
            clear_terminal()
        elif select == "f":
            schedule.swap_tasks_in_jobdb()
            clear_terminal()
        elif select == "sc":
            clear_terminal()
            print(f"\n\n{schedule.get_schedule_output(lastl=False)}")
            input(f"\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "scp":
            clear_terminal()
            schedule.plot_schedule()
            clear_terminal()
        elif select == "scc":
            clear_terminal()
            schedule.schedleft()
            clear_terminal()
        elif select == "scf":
            clear_terminal()
            schedule.calculate_and_print_free_hours()
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "sf":
            clear_terminal()
            streaks.show_streaks()
            input(f"{colors.YELLOW}\n\n{colors.space*5}Press any key to continue...")
            clear_terminal()
        elif select == "re":
            clear_terminal()
            repetition.show_reminders()
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "s":
            clear_terminal()
            schedule.main()
            clear_terminal()
        elif select == "ro":
            clear_terminal()
            endeavor.show_endeavors()
            input(f"{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "sa":
            clear_terminal()
            try:
                tgbot.pytelbot("🔥 Good Day! May you Seize the day with confidence and purpose! 💪✨")
            except:
                pass
            todaysch = "\n\n"+"your today's schedule is:\n"+schedule.remove_color_codes(schedule.get_schedule_output(lastl=True))
            try:
                tgbot.pytelbot(todaysch)
            except:
                pass
            telegram_status_print()
            start_time = datetime.now()
            start_data = {"start_time": start_time.strftime("%Y-%m-%d %H:%M:%S")}
            with open(start_file, "w") as file:
                json.dump(start_data, file)
        elif select == "ta":
            clear_terminal()
            tasks.taskfile(show=False)
            input("\n\nPress any key to continue...")
            clear_terminal()
        elif select == "cc":
            choices = input(colors.space*7+"Are you sure(y/n)? ")
            if choices.lower() == 'y':
                try: 
                    activity.calculate_and_save_activity_rating()
                    original_stdout = sys.stdout
                    sys.stdout = io.StringIO()
                    activity.calculate_activity_rating()
                    function_output = sys.stdout.getvalue()
                    sys.stdout = original_stdout
                    try:    
                        tgbot.pytelbot(function_output)
                        tgbot.pytelbot("Congrats! what a day to be alive💫💫")
                    except:
                        pass
                    original_stdout = sys.stdout
                    sys.stdout = io.StringIO()
                    schedule.sum_and_show_tag_percentages()
                    print("#work #hours ⏰ 🕒 ")
                    function_output = sys.stdout.getvalue()
                    sys.stdout = original_stdout
                    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
                    function_output_cleaned = ansi_escape.sub('', function_output)
                    try:
                        tgbot.pytelbot(function_output_cleaned)
                    except:
                        pass
                except:
                    clear_terminal()
            else:
                clear_terminal()
        elif select == "tr":
            clear_terminal()
            try:
                goalplanner.tracker_greedy(rint=True)
                estimation.tracker_greedy(rint=True)
                xestimation.tracker_greedy(rint=True)
                lectureplanner.tracker_greedy(rint=True)
                freeplanner.tracker_greedy()
                bookplanner.tracker_greedy(rint=True)
            except:
                print("\n\nERROR: PROCESS UNIDENTIFIED")
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "p":
            clear_terminal()
            project.main()
        elif select == "t":
            clear_terminal()
            estimation.main()
        elif select == "tt":
            clear_terminal()
            xestimation.main()
        elif select == "tb":
            clear_terminal()
            bookplanner.main()
        elif select == "tv":
            clear_terminal()
            lectureplanner.main()
        elif select == "tg":
            clear_terminal()
            goalplanner.main()
        elif select == "tf":
            clear_terminal()
            freeplanner.main()
        elif select == "v":
            clear_terminal()
            videolecture.main()
            clear_terminal()  
        elif select =="td":
            clear_terminal()
            progress.check_today()
            input(f"\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "a":
            clear_terminal()
            activity.main()
        elif select == "nn":
            clear_terminal()
            schedule.edit_notes(files=True)
            clear_terminal()
        elif select == "r":
            clear_terminal()
            repetition.main()
        elif select == "u":
            clear_terminal()
            subjects.main()
        elif select == "b":
            clear_terminal()
            newbook.main()
        elif select == "m":
            clear_terminal()
            flashcard.main()
        elif select == "c":
            clear_terminal()
            calendar.main()
        elif select == "j":
            clear_terminal()
            daycalculator.save_date_to_json()
            daycalculator.save_tilldata()
            clear_terminal()
            print("!day changed, please reload the program\n")
        elif select == "n":
            clear_terminal()
            notes.main()
        elif select == "w":
            clear_terminal()
            weighttracker.main()
        elif select == "y":
            clear_terminal()
            streaks.main()
        elif select == "q":
            clear_terminal()
            break
        else:
            clear_terminal()


if __name__ == '__main__':
    main()
