import Lyrics
import random
import datetime

commands = {'!peter' : 'Lyrics',
            '!brian' : 'Lyrics',
            '!calvin' : 'Lyrics',
            '!david' : 'Lyrics',
            '!will' : 'Lyrics',
            '!interesting' : 'Pulls up interesting facts for you',
            '!activity day' : 'Shows activities in last 24 hours',
            '!activity week' : 'Shows activities in last week'}

def help():

    message = 'Commands:\n'
    for command in commands:
        message += '\t{} : {}\n'.format(command, commands[command])
    return message

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

def record(posts, message, author, discord_bot):

    if author == discord_bot:
        return

    for command in commands:
        if message == command:
            return

    post_data = {
        'content' : str(message),
        'author' : str(author),
        'time' : datetime.datetime.utcnow()
    }
    posts.insert_one(post_data)

def activity_day(posts):

    start = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    end = datetime.datetime.utcnow()
    time_post = posts.find({'time': {'$gte': start, '$lt': end}})

    dictionary = dict()
    total_post = 0
    for post in time_post:
        name = post['author']
        if name in dictionary:
            dictionary[name] += 1
        else:
            dictionary[name] = 1
        total_post += 1

    message = 'Activities in last day:\n'
    for key in dictionary:
        name = str(key)
        percentage = round(dictionary[key] / total_post * 100, 2)
        message += '\t{} : {}%\n'.format(name, percentage)

    return message

def activity_week(posts):

    start = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    end = datetime.datetime.utcnow()
    time_post = posts.find({'time': {'$gte': start, '$lt': end}})

    dictionary = dict()
    total_post = 0
    for post in time_post:
        name = post['author']
        if name in dictionary:
            dictionary[name] += 1
        else:
            dictionary[name] = 1
        total_post += 1

    message = 'Activities in last week:\n'
    for key in dictionary:
        name = key
        percentage = round(dictionary[key] / total_post * 100, 2)
        message += '\t{} : {}%\n'.format(name, percentage)

    return message