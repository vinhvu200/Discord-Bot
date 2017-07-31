import discord
import asyncio
import Action

token = 'MzQwNjk2ODA1MTU3MzcxOTA3.DF6tNg.q3amSFyo47M8vFoOScvp6TOCrGU'

client = discord.Client()

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

    if content.startswith('!peter'):
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

    if response is not None:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, response)

    if message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(token)

