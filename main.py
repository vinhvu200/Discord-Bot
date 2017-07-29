import discord
import asyncio
import random

token = ''

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    CupCakke = ["Daddy better make me choke",
                "My tunnel loves a deep throat",
                "I want to eat your dick",
                "Put it so deep, I can't speak a sentence",
                "Mouth wide open like I was at the dentist",
                "I'mma write my name on his dick",
                "My pussy pink just like salami",
                "My pussy mean, and it's clean",
                "I'm not a squirter, I cream",
                "Ballerina that dick when I spin",
                "Just come put it down my butt",
                "Ride the dick, get my nipples licked",
                "Finna get the dick wet and firm",
                "You better sweat me out of my perm"]

    words = message.content.split()

    grahamFlag = False
    brianFlag = False
    beccaFlag = False
    peterFlag = False
    calvinFlag = False
    willFlag = False

    for word in words:

        if word == "graham" or word == "Graham":
            grahamFlag = True
        if word == "calvin" or word == "Calvin":
            calvinFlag = True
        if word == "brian" or word == "Brian":
            brianFlag = True
        if word == "peter" or word == "Peter":
            peterFlag = True
        if word == "becca" or word == "Becca":
            beccaFlag = True
        if willFlag == "Will" or word == "will":
            willFlag = True

    if grahamFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "Good Shit")
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "10/10")

    if calvinFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "My pussy pink like salami")

    if brianFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "Mouth wide open like I was at the dentist")

    if peterFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "I'm not a squirter I cream")

    if beccaFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "Keep it smelling like baby wipes")
    if willFlag == True:
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, "Ballerina that dick when I spin")

    word = message.content.lower()

    if word == '!cupcakke':
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        await client.edit_message(tmp, CupCakke[random.randint(0,len(CupCakke))])

    #if message.content.startswith('!'):

        #tmp = await client.send_message(message.channel, 'Calculating messages...')
        #await client.edit_message(tmp,'sorry @chris#9244')

        #counter = 0
        #tmp = await client.send_message(message.channel, 'Calculating messages...')
        #async for log in client.logs_from(message.channel, limit=100):
        #    if log.author == message.author:
        #        counter += 1

        #await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(token)

