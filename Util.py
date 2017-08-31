import datetime
from collections import OrderedDict


def get_times(interval, delta):

    if interval == 'day':

        # Calculate utc and real end time
        utc_end = datetime.datetime.utcnow()
        real_end = utc_end - datetime.timedelta(hours=7)

        # Calculate utc and real start time
        utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
        real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

        print('Current : {} --- {}'.format(real_start, real_end))

        # Adjust utc time range with delta
        utc_end = utc_start - datetime.timedelta(days=delta - 1)
        utc_start = utc_start - datetime.timedelta(days=delta)

        # Adjust real time range with delta
        real_end = real_start - datetime.timedelta(days=delta - 1)
        real_start = real_start - datetime.timedelta(days=delta)

        print('Adjusted : {} --- {}'.format(real_start, real_end))

    elif interval == 'week':

        # Calculate utc and real end time
        utc_end = datetime.datetime.utcnow()
        real_end = utc_end - datetime.timedelta(hours=7)

        # Calculate utc and real start time
        utc_start = utc_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)
        real_start = real_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)

        print('Current : {} --- {}'.format(real_start, real_end))

        # Adjust utc time range with delta
        utc_end = utc_start - datetime.timedelta(days=(delta - 1) * 7)
        utc_start = utc_start - datetime.timedelta(days=delta * 7)

        # Adjust real time range with delta
        real_end = real_start - datetime.timedelta(days=(delta - 1) * 7)
        real_start = real_start - datetime.timedelta(days=delta * 7)

        print('Adjusted : {} --- {}'.format(real_start, real_end))
    else:
        utc_start = utc_end = real_start = real_end = -1

    return utc_start, utc_end, real_start, real_end


def calculate_daily_activities_percentage(query_results):

    message_count = 0
    activities = dict()

    for query in query_results:
        message_count += 1
        name = query['author']
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    return message_count, sorted_activities


def calculate_daily_activities(query_results):

    messages = [0] * 24
    message_count = 0
    for query in query_results:

        if query['time'].hour - 7 >= 0:
            adjusted = query['time'].hour - 7
        else:
            adjusted = 24 + (query['time'].hour - 7)

        messages[adjusted] += 1
        message_count += 1

    return messages


def calculate_weekly_activities(query_results):

    activities = OrderedDict()
    for query in query_results:

        time = query['time']
        time = time - datetime.timedelta(hours=7)
        day = '{} {} {}'.format(time.month, time.day, time.year)
        string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

        if string_day in activities:
            activities[string_day] += 1
        else:
            activities[string_day] = 1

    return activities


def calculate_weekly_activities_percentage(query_results):

    message_count = 0
    activities = dict()
    for query in query_results:
        message_count += 1
        name = query['author']
        if name in activities:
            activities[name] += 1
        else:
            activities[name] = 1

    for activity in activities:
        activities[activity] = activities[activity] / message_count * 100
    sorted_activities = [(activity, activities[activity]) for activity in
                         sorted(activities, key=activities.get, reverse=True)]

    return sorted_activities