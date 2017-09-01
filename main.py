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
reddit_client = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent=user_agent,
                     username=username)
discord_client = discord.Client()
mongo_client = MongoClient(link)
db = mongo_client.discord_data
messages = db.messages

@discord_client.event
async def on_ready():
    print('Logged in as')
    print(discord_client.user.name)
    print(discord_client.user.id)
    print('------')

    #for server in client.servers:
    #    for channel in server.channels:
    #        print(channel)

@discord_client.event
async def on_message(message):

    if message.author == discord_client.user:
        return

    content = message.content.lower()
    response = None

    Action.record(messages, content, message.author, discord_client.user, message.channel)

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
        response = Action.interesting(reddit_client)
    elif content == '!activity day':
        response = Action.activity_day(messages, 0)
    elif content == '!activity week':
        response = Action.activity_week(messages, 0)
    elif content == '!activity day percentage':
        response = Action.activity_day_percentage(messages, 0)
    elif content == '!activity week percentage':
        response = Action.activity_week_percentage(messages, 0)
    elif 'min sok' in content:
        response = Action.min_sok()
    elif 'good shit' in content:
        response = Action.good_shit()
    elif 'dank' in content:
        response = Action.dank()

    if response is not None:
        tmp = await discord_client.send_message(message.channel, 'Calculating messages...')
        await discord_client.edit_message(tmp, response)

discord_client.run(token)
