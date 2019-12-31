# Work with Python 3.6
import discord
import random
import os
from pycoingecko import CoinGeckoAPI
import re

# Powered by CoinGecko API
cg = CoinGeckoAPI()

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
        if ('win' in message.content) and ('lottery' in message.content):
            await message.channel.send('Statistically, the odds of winning are about 1 in 175 million so I would say no.')
        else:
            await message.channel.send(random.choice(possible_responses))
    # Cryptocurrency price
    elif message.content.startswith('!price'):
        message_list = message.content.split()
        crypto = message_list[message_list.index('!price') + 1]
        result = str(cg.get_price(ids=crypto, vs_currencies='usd'))
        price =  re.findall(r"\d+\.\d{1,2}", result)
        await message.channel.send(crypto +" price is: $" + price[0])
    # Confusion message
    elif message.content == 'what' or message.content == 'wot' or message.content == 'wat':
        await message.channel.send('what')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if __name__ == '__main__':
    import config
    client.run(config.token)