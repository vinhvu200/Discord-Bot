import discord
import Action
import praw
import datetime
from pymongo import MongoClient

# Getting credentials
f = open('Stuff.txt', 'r')
token = f.readline()[:-1]
client_id = f.readline()[:-1]
client_secret = f.readline()[:-1]
password = f.readline()[:-1]
user_agent = 'stuff'
username = f.readline()
f.close()

# Getting client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent=user_agent,
                     username=username)
client = discord.Client()
client_2 = MongoClient()
db = client_2.pymongo_test
posts = db.posts

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    content = message.content.lower()
    response = None

    if content.startswith('!help'):
        response = Action.help()
    elif content.startswith('!peter'):
        response = Action.peter()
    elif content.startswith('!brian'):
        response = Action.brian()
    elif content.startswith('!becca'):
        response = Action.becca()
    elif content.startswith('!david'):
        response = Action.david()
    elif content.startswith('!will'):
        response = Action.will()
    elif content.startswith('!calvin'):
        response = Action.calvin()
    elif content.startswith('!graham'):
        response = Action.graham()
    elif content.startswith('!interesting'):
        response = Action.interesting(reddit)
    elif content.startswith('!record'):
        Action.record(posts, content, message.author)
    elif content.startswith('!pull'):

        start = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        end = datetime.datetime.utcnow()

        time_post = posts.find({'time': {'$gte': start, '$lt': end}})

        dictionary = dict()
        total_post = 0
        for post in time_post:
            print(post)
            name = post['author']
            if name in dictionary:
                dictionary[name] += 1
            else:
                dictionary[name] = 1
            total_post += 1
        print(dictionary)

        for key in dictionary:
            print(key)
            print((round(dictionary[key] / total_post * 100, 2)))
    elif content.startswith('!activity day'):
        response = Action.activity_day(posts)
    elif content.startswith('!activity week'):
        response = Action.activity_week(posts)

    if response is not None:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, response)

client.run(token)