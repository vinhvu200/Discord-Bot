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
        user = ''
        vinhs_post = posts.find_one({'author': user})
        time = vinhs_post['time']
        print(time)
        #reformatted_time = datetime.datetime.strptime(time, '%Y %m %d %H %M')

    if response is not None:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, response)

client.run(token)