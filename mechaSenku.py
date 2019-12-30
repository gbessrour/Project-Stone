# Work with Python 3.6
import discord
import random
import os

# Function to convert number into coin side 
def numbers_to_side(argument): 
	switcher = { 
		1: "heads", 
		2: "tails", 
	} 
	return switcher.get(argument, "nothing") 
# 8-ball responses
possible_responses = [
    'That is a resounding no',
    'It is not looking likely',
    'Too hard to tell',
    'It is quite possible',
    'Definitely',
]
# enter bot token here
TOKEN = 
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # Simple welcome message
    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}. How can Mecha Senku assist you today?'.format(message)
        await message.channel.send(msg)
    # Dice roll
    elif message.content.startswith('!dice'):
        dice = random.randint(1, 6)
        filename = "dice " + str(dice) + ".png"
        dicename = os.path.join('dice', filename)
        await message.channel.send('You rolled ' + str(dice), file=discord.File(dicename))
    # Coin flip
    elif message.content.startswith('!coin'):
        coin = random.randint(1,2)
        filename = numbers_to_side(coin) + ".jpg"
        coinname = os.path.join('coin', filename)
        await message.channel.send('You got ' + numbers_to_side(coin), file=discord.File(coinname))
    # Dad Jokes
    elif (message.content.startswith('I\'m')) or (message.content.startswith('I am')):
        if message.content.startswith('I\'m'):
            dadjoke = message.content.replace('I\'m', '')
        elif message.content.startswith('I am'):
            dadjoke = message.content.replace('I am', '')
        msg = 'Hi' + dadjoke + '. I\'m dad!'
        await message.channel.send(msg)
    # Eight ball
    elif message.content.startswith('!8ball'):
        await message.channel.send(random.choice(possible_responses))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN) 