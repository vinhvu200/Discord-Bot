import Lyrics
import random
import datetime

def help():

    return 'Commands:\n' \
              '\t!peter\n' \
              '\t!brian\n' \
              '\t!calvin\n' \
              '\t!david\n' \
              '\t!will\n' \
              '\t!interesting\n' \
              '\t!help'

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

def record(posts, message, author):

    time = datetime.datetime.now()
    new_time = time.strftime('%Y %m %d %H %M')
    #reformatted_time = datetime.datetime.strptime(new_time, '%Y %m %d %H %M')

    post_data = {
        'content' : str(message),
        'author' : str(author),
        'time' : new_time
    }

    print(post_data)
    result = posts.insert_one(post_data)
    #print('One post: {0}'.format(result.inserted_id))
