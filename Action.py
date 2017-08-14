import Lyrics
import random
import datetime

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

def record(posts, message, author, discord_bot, channel):

    if author == discord_bot:
        return

    for command in commands:
        if message == command:
            return

    try:

        post_data = {
            'content' : str(message),
            'author' : str(author),
            'time' : datetime.datetime.utcnow(),
            'channel' : str(channel)
        }
        posts.insert_one(post_data)
    except Exception:
        return 'Vinhs an idiot. Command failed'

def activity_day(posts):

    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(hours=end.hour, minutes=end.minute)

    try:
        time_posts = posts.find({'time': {'$gte': start, '$lt': end}, 'channel': 'skype'})
        dictionary = dict()
        total_posts = 0
        for post in time_posts:
            name = post['author']
            if name in dictionary:
                dictionary[name] += 1
            else:
                dictionary[name] = 1
            total_posts += 1

        message = 'Activities in last day:\n'
        sorted_activities = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
        for name, percentage in sorted_activities:
            message += '\t{}   --   {}%\n'.format(name, round(percentage / total_posts * 100, 2))
    except Exception:
        return 'Vinhs an idiot. Command failed'

    return message

def activity_week(posts):

    start = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    end = datetime.datetime.utcnow()
    message = 'Activities in last week:\n'
    dictionary = dict()
    total_posts = 0

    try:
        time_posts = posts.find({'time': {'$gte': start, '$lt': end}, 'channel': 'skype'})
        for post in time_posts:
            name = post['author']
            if name in dictionary:
                dictionary[name] += 1
            else:
                dictionary[name] = 1
            total_posts += 1

        sorted_activities = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
        for name, percentage in sorted_activities:
            message += '\t{}   --   {}%\n'.format(name, round(percentage / total_posts * 100, 2))

    except Exception:
        return 'Vinhs an idiot. Command failed'

    return message

def min_sok():
    return "@Vinh#9804 heard min sok"

def dank():
    return "D A N K"

def good_shit():
    return '10/10'

def detail_day(posts):
    utc_end = datetime.datetime.utcnow()
    real_end = utc_end - datetime.timedelta(hours=7)

    utc_start = utc_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)
    real_start = real_end - datetime.timedelta(hours=real_end.hour, minutes=real_end.minute)

    messages = [0] * 24

    try:
        query_results = posts.find({'time': {'$gte': utc_start, '$lt': utc_end}, 'channel': 'skype'})
    except Exception:
        return 'Could not retrieve from database. Vinh failed you'

    message_count = 0
    for query in query_results:

        adjusted = 0
        if query['time'].hour - 7 >= 0:
            adjusted = query['time'].hour - 7
        else:
            adjusted = 24 - query['time'].hour - 7

        messages[adjusted] += 1
        message_count += 1

    message = 'Message count per hour for {} . {} . {}\n'.format(real_start.month,
                                                                 real_start.day,
                                                                 real_start.year)
    for x in range(0, 24):
        message += '\t{}:00   ---   {}\n'.format(x, messages[x])

    return message

def detail_week(posts):

    message = 'Message count in the last week\n'
    adjusted_end_time = datetime.datetime.utcnow() - datetime.timedelta(hours=7)
    adjusted_start_time = adjusted_end_time - datetime.timedelta(hours=adjusted_end_time.hour)
    real_end_time = datetime.datetime.utcnow()
    real_start_time = real_end_time - datetime.timedelta(hours=adjusted_end_time.hour)

    try:
        message_count = 0
        query_results = posts.find({'time': {'$gte': real_start_time, '$lt': real_end_time},
                                    'channel': 'skype'})
        for results in query_results:
            message_count += 1
        message += '\t{} . {} . {}   --   {}\n'.format(adjusted_start_time.month,
                                                   adjusted_start_time.day,
                                                   adjusted_start_time.year,
                                                   message_count)

        for x in range(0,6):
            message_count = 0
            adjusted_end_time = adjusted_end_time - datetime.timedelta(days=1)
            adjusted_start_time = adjusted_start_time - datetime.timedelta(days=1)
            real_end_time = real_end_time - datetime.timedelta(days=1)
            real_start_time = real_start_time - datetime.timedelta(days=1)

            query_results = posts.find({'time': {'$gte': real_start_time, '$lt': real_end_time},
                                        'channel': 'skype'})
            for results in query_results:
                message_count += 1
            message += '\t{} . {} . {}   --   {}\n'.format(adjusted_start_time.month,
                                                         adjusted_start_time.day,
                                                         adjusted_start_time.year,
                                                         message_count)
    except Exception:
        return 'Vinhs an idiot. Command failed'

    return message