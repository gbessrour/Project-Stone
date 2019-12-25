# Work with Python 3.6
import discord
import random
import os

# Functions
# Function to convert number into coin side 
def numbers_to_side(argument): 
	switcher = { 
		1: "heads", 
		2: "tails", 
	} 
	return switcher.get(argument, "nothing") 

TOKEN =  # enter bot token here

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
    # Error message
    else:
        await message.channel.send('Try again', file=discord.File('wrong.gif'))
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)