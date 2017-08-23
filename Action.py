import Lyrics
import random
import datetime
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
            '!detail day' : '',
            '!detail week' : ''}

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
           '\t!activity day : Activities percentage in last 24 hours\n' \
           '\t!activity week : Activities percentage in last week\n' \
           '\t!detail day : Activities by hours of that day\n' \
           '\t!detail week : Activities by days of the last week'

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
        #'channel' : str(channel)
        'channel' : 'skype'
    }

    try:
        messages_collection.insert_one(post_data)
    except Exception:
        return 'Vinhs an idiot. Command failed'

def activity_day(messages_collection):

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

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

    message = 'Activities for {} . {} . {}:\n' \
              '----------------------------\n'.format(real_start.month,
                                                      real_start.day,
                                                      real_start.year)
    for name, percentage in sorted_activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))
    return message

def activity_week(messages_collection):

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)

    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

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

    message = 'Activities between {}.{}.{} -- {}.{}.{}:\n' \
              '----------------------------\n'.format(real_start.month, real_start.day,
                                                      real_start.year, real_end.month,
                                                      real_end.day, real_end.year)
    for name, percentage in sorted_activities:
        message += '{}   --   {}%\n'.format(name, round(percentage, 2))
    return message

def min_sok():
    return "@Vinh#9804 heard min sok"

def dank():
    return "D A N K"

def good_shit():
    return '10/10'

def detail_day(messages_collection):

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

    messages = [0] * 24
    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception as e:
        print(e)
        return 'Could not retrieve from database. Vinh failed you'

    message_count = 0
    for query in query_results:

        adjusted = 0
        if query['time'].hour - 7 >= 0:
            adjusted = query['time'].hour - 7
        else:
            adjusted = 24 + (query['time'].hour - 7)

        messages[adjusted] += 1
        message_count += 1

    message = 'Message count per hour for {} . {} . {}\n'.format(real_start.month,
                                                                 real_start.day,
                                                                 real_start.year)
    for x in range(0, 24):
        message += '\t{}:00   ---   {}\n'.format(x, messages[x])

    return message

def detail_week(messages_collection):

    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(days=6, hours=real_end.hour, minutes=real_end.minute)

    activities = OrderedDict()

    try:
        query_results = messages_collection.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    for query in query_results:

        time = query['time']
        time = time - datetime.timedelta(hours=7)
        day = '{} {} {}'.format(time.month, time.day, time.year)
        string_day = datetime.datetime.strptime(day, '%m %d %Y').strftime('%A')

        if string_day in activities:
            activities[string_day] += 1
        else:
            activities[string_day] = 1

    message = 'Message count: {}.{}.{} -- {}.{}.{}\n' \
              '------------------------------\n'.format(real_start.month, real_start.day,
                                                        real_start.year, real_end.month,
                                                        real_end.day, real_end.year)

    for day in activities:
        message += '{} -- {}\n'.format(day, activities[day])

    return message