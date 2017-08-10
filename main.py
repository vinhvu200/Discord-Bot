import discord
import Action
import praw
from pymongo import MongoClient

# Getting credentials
f = open('Stuff.txt', 'r')
token = f.readline()[:-1]
client_id = f.readline()[:-1]
client_secret = f.readline()[:-1]
password = f.readline()[:-1]
user_agent = 'stuff'
username = f.readline()[:-1]
link = f.readline()
f.close()

# Getting client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent=user_agent,
                     username=username)
client = discord.Client()
client_2 = MongoClient(link)
db = client_2.pymongo_test
posts = db.posts

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #for server in client.servers:
    #    for channel in server.channels:
    #        print(channel)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    content = message.content.lower()
    response = None

    Action.record(posts, content, message.author, client.user, message.channel)

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
    elif content.startswith('!activity day'):
        response = Action.activity_day(posts)
    elif content.startswith('!activity week'):
        response = Action.activity_week(posts)
    elif 'min sok' in content:
        response = Action.min_sok()

    if response is not None:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, response)

client.run(token)