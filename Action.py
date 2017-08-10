import Lyrics
import random
import datetime

commands = {'!peter' : 'Lyrics',
            '!brian' : 'Lyrics',
            '!calvin' : 'Lyrics',
            '!david' : 'Lyrics',
            '!will' : 'Lyrics',
            '!becca' : 'Lyris',
            '!interesting' : 'Pulls up interesting facts for you',
            '!activity day' : 'Shows activities in last 24 hours',
            '!activity week' : 'Shows activities in last week',
            '!detail' : ''}

def help():

    return 'Commands:\n' \
           '\t!peter : Lyrics\n' \
           '\t!brian : Lyrics\n' \
           '\t!calvin : Lyrics\n' \
           '\t!david : Lyrics\n' \
           '\t!will : Lyrics\n' \
           '\t!interesting : Pulls up interesting facts for you\n' \
           '\t!activity day : Shows activities in last 24 hours\n' \
           '\t!activity week : Show activities in last week'

def peter():
    return Lyrics.Astley[random.randint(0, len(Lyrics.Astley)-1)]

def brian():
    return Lyrics.Lazytown[random.randint(0, len(Lyrics.Lazytown)-1)]

def becca():
    return Lyrics.NSN[random.randint(0, len(Lyrics.NSN)-1)]

def will():
    return Lyrics.CupCakke[random.randint(0, len(Lyrics.CupCakke)-1)]

def david():
    return Lyrics.Spongebob[random.randint(0, len(Lyrics.Spongebob)-1)]

def calvin():
    return Lyrics.Desiigner[random.randint(0, len(Lyrics.Desiigner)-1)]

def graham():
    return Lyrics.Hokey_pokey[random.randint(0, len(Lyrics.Hokey_pokey)-1)]

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
        pass

def activity_day(posts):

    start = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    end = datetime.datetime.utcnow()
    time_posts = posts.find({'time': {'$gte': start, '$lt': end}})

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
        message += '\t{}   --   {}%\n'.format(name, percentage)

    return message

def activity_week(posts):

    start = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    end = datetime.datetime.utcnow()
    message = 'Activities in last week:\n'
    dictionary = dict()
    total_posts = 0

    try:
        time_posts = posts.find({'time': {'$gte': start, '$lt': end}})
        for post in time_posts:
            name = post['author']
            if name in dictionary:
                dictionary[name] += 1
            else:
                dictionary[name] = 1
            total_posts += 1

        sorted_activities = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
        for name, percentage in sorted_activities:
            message += '\t{}   --   {}%\n'.format(name, percentage)

    except Exception:
        pass

    return message

def min_sok():
    return "Vinh heard min sok"

def detail_day(posts):

    end_time = datetime.datetime.utcnow()
    hour_count = end_time.hour
    minutes = end_time.minute
    message_count = 0
    start_time = end_time - datetime.timedelta(minutes=minutes)

    try:
        query_results = posts.find({'time': {'$gte': start_time, '$lt': end_time}})
        for result in query_results:
            message_count += 1

        print('Hour: {} -- Message Count: {}'.format(start_time.hour, message_count))

        end_time = end_time - datetime.timedelta(minutes=end_time.minute)
        start_time = start_time - datetime.timedelta(hours=1)

        for x in range(0, hour_count):
            message_count = 0
            query_results = posts.find({'time': {'$gte': start_time, '$lt': end_time}, 'author': 'vinh#9804'})
            for result in query_results:
                message_count += 1

            print('Hour: {} -- Message Count: {}'.format(start_time.hour, message_count))

            end_time = end_time - datetime.timedelta(hours=1)
            start_time = start_time - datetime.timedelta(hours=1)
    except Exception:
        pass

    return None

def detail_week(posts):

    message = 'Message counts per day\n'
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=end_time.hour, minutes=end_time.minute)
    message_count = 0
    day = 7

    try:
        query_results = posts.find({'time': {'$gte': start_time, '$lt': end_time}})
        for result in query_results:
            message_count += 1
        print('Day {} -- Message Count : {}'.format(day, message_count))
        message += '\tDay {}  --  {}\n'.format(day, message_count)
        day -= 1

        while day > 0:
            message_count = 0
            end_time = end_time - datetime.timedelta(days=1)
            start_time = start_time - datetime.timedelta(days=1)

            query_results = posts.find({'time': {'$gte': start_time, '$lt': end_time}})

            for result in query_results:
                message_count += 1
            print('Day {} -- Message Count : {}'.format(day, message_count))
            message += '\tDay {}  --  {}\n'.format(day, message_count)
            day -= 1
    except Exception:
        pass

    return message