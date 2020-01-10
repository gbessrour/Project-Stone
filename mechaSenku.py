# Work with Python 3.6
import discord
import random
import os
from pycoingecko import CoinGeckoAPI
import re
from jikanpy import Jikan
from bs4 import BeautifulSoup
import urllib
import json

# Powered by CoinGecko API
cg = CoinGeckoAPI()

#Powered by Jikan Unofficial MAL Anime API
jikan = Jikan()

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

token = os.environ['token']

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
    elif (message.content.startswith('I\'m ')) or (message.content.startswith('I am ') or (message.content.startswith('Im '))):
        if message.content.startswith('I\'m '):
            dadjoke = message.content.replace('I\'m ', '')
        elif message.content.startswith('I am '):
            dadjoke = message.content.replace('I am ', '')
        elif message.content.startswith('Im '):
            dadjoke = message.content.replace('Im ', '')
        msg = 'Hi ' + dadjoke + '. I\'m dad!'
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
    elif message.content.lower() == 'what' or message.content.lower() == 'wot' or message.content.lower() == 'wat' or message.content.lower() =='nani':
        await message.channel.send(message.content)

    #PubSubs on sale or not
    elif message.content.startswith('!pubsub'):
        req = urllib.request.Request('http://arepublixchickentendersubsonsale.com')
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        if ('<!-- onsale:no -->') in respData:
            answer = "Pub subs are NOT on sale :("
        elif('<!-- onsale:yes -->') in respData:
            answer = "Pub subs ARE on sale my dudes!!!"
            await message.channel.send(file=discord.File(os.path.join('Reacts', 'excited_deku.gif')))
        await message.channel.send(answer)
    
    #Anime
    elif message.content.startswith('!anime'):
        anime_list = message.content.split()
        param = anime_list[anime_list.index('!anime') + 1]
        second_param = str(anime_list[2:])
        if(param == 'name'):
            anime = jikan.search(search_type= 'anime', query= second_param)
            data = json.dumps(anime)
            loaded_data = json.loads(data)
            anime_title = loaded_data['results'][0]['title']
            year_released = str(loaded_data['results'][0]['start_date'])
            synopsis = loaded_data['results'][0]['synopsis']            
            url = loaded_data['results'][0]['url']
            image_result = loaded_data['results'][0]['image_url']
            episodes = loaded_data['results'][0]['episodes']
            score = loaded_data['results'][0]['score']
            embed = discord.Embed(title=str(anime_title), value=str(anime_title), inline=False)
            embed.add_field(name="Score", value=score, inline=False)
            embed.add_field(name="Synopsis", value=synopsis, inline=False)
            embed.add_field(name="Number of Episdoes", value=episodes, inline=False)
            embed.add_field(name="Year Released", value=year_released[0:4], inline=False)
            embed.set_image(url=image_result)
            embed.add_field(name="URL", value=url, inline=False)
        elif(param == 'seasonal'):
            third_param = anime_list[anime_list.index('!anime') + 3]
            result = jikan.season(year= int(third_param), season= second_param)
        await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
