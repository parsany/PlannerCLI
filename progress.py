import os
from estimations import estimation, freeplanner, xestimation, bookplanner, lectureplanner, goalplanner
from uptils import colors
from datetime import datetime

SCH_TXT = os.path.join(colors.notes_file, 'plan.md')

def check_trackers(length=20,rint=True):
    est,esd = estimation.calculate_tracker_totals()
    fst,fsd = freeplanner.calculate_tracker_totals()
    xst,xsd = xestimation.calculate_tracker_totals()
    bst,bsd = bookplanner.calculate_tracker_totals()
    lst,lsd = lectureplanner.calculate_tracker_totals()
    lst = lst/60*3.14
    lsd = lsd/60*3.14
    gst,gsd = goalplanner.calculate_tracker_totals()
    sum_trackers = est+fst+xst+bst+gst+lst
    sum_done = esd+fsd+xsd+bsd+gsd+lsd
    total_percentage = sum_done / sum_trackers if sum_trackers > 0 else 0
    if rint:
        filled_length = int(length * total_percentage)
        bar = '[' + '█' * filled_length + ' ' * (length - filled_length) + ']'
        print(f"{colors.space*7}{colors.CYAN}Task Progress Level: {colors.WWITE} {bar} ({total_percentage:.2%}) {colors.PURPLE} (td for percentiles) {colors.RESET}")
    else:
        return sum_trackers,sum_done


def check_today(length=20):
    workperday = estimation.tracker_greedy(rint=False)
    bookperday = bookplanner.tracker_greedy(rint=False)
    exerperday = xestimation.tracker_greedy(rint=False)
    lectperday = lectureplanner.tracker_greedy(rint=False)/60*3.14
    goalperday = goalplanner.tracker_greedy(rint=False)
    freeperday = freeplanner.tracker_greedy(rint=False)

    day_names = {
        0: 'MON',
        1: 'TUE',
        2: 'WED',
        3: 'THUR',
        4: 'FRI',
        5: 'SAT',
        6: 'SUN'
    }

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    free_activities_hours = {day_name: 0 for day_name in day_names.values()}

    for line in lines:
        line = line.strip()
        if line.startswith('#') and line[2:] in day_names.values():
            current_day_name = line[2:]
        elif current_day_name and line:
            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free time":
                free_activities_hours[current_day_name] += activity_hours

    total_sum_free = sum(free_activities_hours.values())
    print("\n\n")
    percentweek = 0 
    for day_name in day_names.values():
        workamount_free = workperday * 7 / total_sum_free * free_activities_hours[day_name]
        bookamount_free = bookperday * 7 / total_sum_free * free_activities_hours[day_name]
        exerciseam_free = exerperday * 7 / total_sum_free * free_activities_hours[day_name]
        lecturetim_free = lectperday * 7 / total_sum_free * free_activities_hours[day_name]
        goaltrackm_free = goalperday * 7 / total_sum_free * free_activities_hours[day_name]
        freetratim_free = freeperday * 7 / total_sum_free * free_activities_hours[day_name]

        sum_today = workamount_free + bookamount_free + exerciseam_free + freetratim_free + goaltrackm_free + lecturetim_free
        sum_trackers,sum_done = check_trackers(length=20,rint=False)

        percentday = sum_today/sum_trackers*100
        percentweek += percentday
        print(f"{colors.space*2}{colors.YELLOW}{day_name} -{colors.PURPLE} work amount:{sum_today:.2f}{colors.YELLOW} | {colors.CYAN}percentage: {percentday:.2f}%{colors.RESET}")
    print(f"\n{colors.space*4}{colors.CYAN}>{colors.WWITE}percent week is {colors.CYAN}{percentweek:.2f}%")