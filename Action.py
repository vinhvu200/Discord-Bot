import Lyrics
import random
import datetime
import Util
from collections import OrderedDict

commands = {'!peter' : 'Lyrics',
            '!brian' : 'Lyrics',
            '!calvin' : 'Lyrics',
            '!david' : 'Lyrics',
            '!will' : 'Lyrics',
            '!becca' : 'Lyrics',
            '!graham' : 'Lyrics',
            '!interesting' : 'Pulls up interesting facts for you',
            '!activity day' : 'Shows activities in last 24 hours',
            '!activity week' : 'Shows activities in last week',
            '!activity day percentage' : '',
            '!activity week percentage' : ''}

def help():

    return 'Commands:\n' \
           '\t!peter : Lyrical Genius\n' \
           '\t!brian : Lyrical Genius\n' \
           '\t!becca : Lyrical Genius\n' \
           '\t!calvin : Lyrical Genius\n' \
           '\t!david : Lyrical Genius\n' \
           '\t!will : Lyrical Genius\n' \
           '\t!graham : Lyrical Genius\n' \
           '\t!interesting : Interesting facts for you\n' \
           '\t!activity day : Activities in the current day\n' \
           '\t!activity week : Activities in the current week\n' \
           '\t!activity day percentage : Percentage of user\'s activity for current day\n' \
           '\t!activity week percentage : Percentage of user\'s activity for last week'

def peter():
    return Lyrics.Peter[random.randint(0, len(Lyrics.Peter)-1)]

def brian():
    return Lyrics.Brian[random.randint(0, len(Lyrics.Brian)-1)]

def becca():
    return Lyrics.Becca[random.randint(0, len(Lyrics.Becca)-1)]

def will():
    return Lyrics.Will[random.randint(0, len(Lyrics.Will)-1)]

def david():
    return Lyrics.David[random.randint(0, len(Lyrics.David)-1)]

def calvin():
    return Lyrics.Calvin[random.randint(0, len(Lyrics.Calvin)-1)]

def graham():
    return Lyrics.Graham[random.randint(0, len(Lyrics.Graham)-1)]

def interesting(reddit):

    count = 0
    rand = random.randint(0, 29)
    prefix_1 = "Did you know..."
    prefix_2 = "Bet you didn't know..."
    interesting_prefix = [prefix_1, prefix_2]

    subreddit = reddit.subreddit('TodayILearned').hot(limit=30)
    for submission in subreddit:
        if count == rand:
            prefix_index = count % 2
            return submission.title.replace('TIL', interesting_prefix[prefix_index])
            break
        count = count + 1

def record(messages_collection, message, author, discord_bot, channel):

    if author == discord_bot:
        return

    for command in commands:
        if message == command:
            return

    post_data = {
        'content' : str(message),
        'author' : str(author),
        'time' : datetime.datetime.utcnow(),
        'channel' : str(channel)
    }

    try:
        messages_collection.insert_one(post_data)
    except Exception:
        return 'Vinhs an idiot. Command failed'


def min_sok():
    return "@Vinh#9804 heard min sok"


def dank():
    return "D A N K"


def good_shit():
    return '10/10'


def activity_day(messages_collection, delta):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception as e:
        print(e)
        return 'Could not retrieve from database. Vinh failed you'

    # Get hourly activities
    activities_by_hours = Util.calculate_daily_activities(query_results)

    # Format message
    message = 'Message count per hour for {} . {} . {}\n'.format(real_start.month,
                                                                 real_start.day,
                                                                 real_start.year)
    for x in range(0, 24):
        message += '\t{}:00   ---   {}\n'.format(x, activities_by_hours[x])

    return message


def activity_day_percentage(messages_collection, delta):

    # Get appropriate time range
    interval = 'day'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception as e:
        print(e)
        return 'Could not retrieve from database. Vinh failed you'

    # Calculate message count and activities with query_results
    message_count, activities = Util.calculate_daily_activities_percentage(query_results)

    # Format message
    message = 'Activities for {} . {} . {}:\n' \
              '----------------------------\n'.format(real_start.month,
                                                      real_start.day,
                                                      real_start.year)
    for name, percentage in activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))
    return message


def activity_week(messages_collection, delta):

    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    # Get weekly activities
    activities = Util.calculate_weekly_activities(query_results)

    # Format Message
    message = 'Message count: {}.{}.{} -- {}.{}.{}\n' \
              '------------------------------\n'.format(real_start.month, real_start.day,
                                                        real_start.year, real_end.month,
                                                        real_end.day, real_end.year)
    for day in activities:
        message += '{} -- {}\n'.format(day, activities[day])

    return message


def activity_week_percentage(messages_collection, delta):

    # Get appropriate time range
    interval = 'week'
    utc_start, utc_end, real_start, real_end = Util.get_times(interval, delta)

    # Attempt to query by dates
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    activities = Util.calculate_weekly_activities_percentage(query_results)

    message = 'Activities between {}.{}.{} -- {}.{}.{}:\n' \
              '----------------------------\n'.format(real_start.month, real_start.day,
                                                      real_start.year, real_end.month,
                                                      real_end.day, real_end.year)
    for name, percentage in activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))
    return message
