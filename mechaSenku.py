# Work with Python 3.6
import discord
from discord.ext import commands
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

# Greetings
greetings = [
    'Hi ',
    'Hi there ',
    'Hello ',
    'Hey ',
    'Hey there ',
]

token = os.environ['token']

#client = discord.Client()
bot = commands.Bot(command_prefix = '!')

# global variable
dad_response = False

# Simple welcome message
@bot.command(pass_context=True)
async def hello(ctx):
    msg = 'Hello {0.mention}. How can Mecha Senku assist you today?'.format(ctx.message.author)
    await ctx.send(msg)

# Dice roll
@bot.command(pass_context=True)
async def dice(ctx):
    dice = random.randint(1, 6)
    filename = "dice " + str(dice) + ".png"
    dicename = os.path.join('dice', filename)
    await ctx.send('You rolled ' + str(dice), file=discord.File(dicename))

# Coin flip
@bot.command(pass_context=True)
async def coin(ctx):
    coin = random.randint(1,2)
    filename = numbers_to_side(coin) + ".jpg"
    coinname = os.path.join('coin', filename)
    await ctx.send('You got ' + numbers_to_side(coin), file=discord.File(coinname))

# Eight ball
@bot.command(pass_context=True, aliases=['8ball'])
async def eight_ball(ctx):
    if ('win' in ctx.message.content) and ('lottery' in ctx.message.content):
        await ctx.send('Statistically, the odds of winning are about 1 in 175 million so I would say no.')
    else:
        await ctx.send(random.choice(possible_responses))

# Cryptocurrency price
@bot.command(pass_context=True)
async def price(ctx):
    message_list = ctx.message.content.split()
    crypto = message_list[message_list.index('!price') + 1]
    result = str(cg.get_price(ids=crypto, vs_currencies='usd'))
    price =  re.findall(r"\d+\.\d{1,2}", result)
    await ctx.send(crypto +" price is: $" + price[0])

# PubSubs on sale or not
@bot.command(pass_context=True)
async def pubsub(ctx):
    req = urllib.request.Request('http://arepublixchickentendersubsonsale.com')
    resp = urllib.request.urlopen(req)
    respData = str(resp.read())
    if ('<!-- onsale:no -->') in respData:
        answer = "Pub subs are NOT on sale :("
        await ctx.send(file=discord.File(os.path.join('Reacts', 'sad_deku.gif')))
    elif('<!-- onsale:yes -->') in respData:
        answer = "Pub subs ARE on sale my dudes!!!"
        await ctx.send(file=discord.File(os.path.join('Reacts', 'excited_deku.gif')))
    await ctx.send(answer)

# Anime search
@bot.command(pass_context=True)
async def anime(ctx):
    anime_list = ctx.message.content.split()
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
        embed.add_field(name="Number of Episodes", value=episodes, inline=False)
        embed.add_field(name="Year Released", value=year_released[0:4], inline=False)
        embed.set_image(url=image_result)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embed=embed)
    elif(param == 'season'):
        second_param = anime_list[anime_list.index('!anime') + 2] #Remember to change this back to !anime in MechaSenku
        third_param = anime_list[anime_list.index('!anime') + 3] #Remember to change this back to !anime in MechaSenku
        
        result = jikan.season(year= int(third_param), season= second_param)
        data = json.dumps(result)
        loaded_data = json.loads(data)
        
        for i in range(0,5):
            randNum = random.randint(0,len(loaded_data["anime"]))

            #Skip showing animes that are continuing when asking about a specific season  
            if loaded_data["anime"][randNum]["continuing"]:
                continue 

            anime_title = loaded_data["anime"][randNum]["title"]
            anime_score = loaded_data["anime"][randNum]["score"]
            anime_episodes = loaded_data["anime"][randNum]["episodes"]
            anime_synopsis = loaded_data["anime"][randNum]["synopsis"]
            image_result = loaded_data['anime'][randNum]['image_url']

            embed = discord.Embed(title=anime_title, value=second_param +" "+ str(third_param), inline=False)
            embed.add_field(name="Score",value=anime_score, inline=True)
            embed.add_field(name="Number of Episodes",value=anime_episodes, inline=False)
            
            for j in range(0,len(loaded_data["anime"][randNum]["genres"])):
                embed.add_field(name="Genre", value= loaded_data["anime"][randNum]["genres"][j]["name"], inline=True)            
           
            if len(anime_synopsis) > 1023:
                embed.add_field(name="Synopsis",value=anime_synopsis[:1023], inline=False)
            else:
                embed.add_field(name="Synopsis",value=anime_synopsis, inline=False)   
           
            embed.set_image(url=image_result)
            await ctx.send(embed=embed)

# Manga search
@bot.command(pass_context=True)
async def manga(ctx):
    await ctx.send("Manga Search coming next patch!!! :D")
    

@bot.event
async def on_message(message):
    global dad_response
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    # Dad Jokes
    elif (message.content.startswith('I\'m ')) or (message.content.startswith('I am ') or (message.content.startswith('Im '))):
        if message.content.startswith('I\'m '):
            dadjoke = message.content.replace('I\'m ', '')
        elif message.content.startswith('I am '):
            dadjoke = message.content.replace('I am ', '')
        elif message.content.startswith('Im '):
            dadjoke = message.content.replace('Im ', '')
        msg = random.choice(greetings) + dadjoke + '. I\'m dad!'
        await message.channel.send(msg)

        dad_response = True
        
    # Confusion message
    elif message.content.lower() == 'what' or message.content.lower() == 'wot' or message.content.lower() == 'wat' or message.content.lower() =='nani':
        await message.channel.send(message.content)

    # Dad joke response
    elif dad_response == True and message.author != bot.user:
        if 'fuck' in message.content.lower() or 'no ' in message.content.lower() or message.content.lower() == 'no':
            await message.channel.send('no u')
        elif 'thank' in message.content.lower():
            await message.channel.send('You\'re welcome, ' + message.author.display_name)
        dad_response = False
        
    # #Anime
    # elif message.content.startswith('!anime'):
    #     anime_list = message.content.split()
    #     param = anime_list[anime_list.index('!anime') + 1]
    #     second_param = str(anime_list[2:])
    #     if(param == 'name'):
    #         anime = jikan.search(search_type= 'anime', query= second_param)
    #         data = json.dumps(anime)
    #         loaded_data = json.loads(data)
    #         anime_title = loaded_data['results'][0]['title']
    #         year_released = str(loaded_data['results'][0]['start_date'])
    #         synopsis = loaded_data['results'][0]['synopsis']            
    #         url = loaded_data['results'][0]['url']
    #         image_result = loaded_data['results'][0]['image_url']
    #         episodes = loaded_data['results'][0]['episodes']
    #         score = loaded_data['results'][0]['score']
    #         embed = discord.Embed(title=str(anime_title), value=str(anime_title), inline=False)
    #         embed.add_field(name="Score", value=score, inline=False)
    #         embed.add_field(name="Synopsis", value=synopsis, inline=False)
    #         embed.add_field(name="Number of Episdoes", value=episodes, inline=False)
    #         embed.add_field(name="Year Released", value=year_released[0:4], inline=False)
    #         embed.set_image(url=image_result)
    #         embed.add_field(name="URL", value=url, inline=False)
    #     elif(param == 'seasonal'):
    #         third_param = anime_list[anime_list.index('!anime') + 3]
    #         result = jikan.season(year= int(third_param), season= second_param)
    #     await message.channel.send(embed=embed)

    # JoJo Reference?
    if 'jojo' in message.content.lower() or 'jojo\'s' in message.content.lower() or 'jojos' in message.content.lower():
        await message.channel.send('Was that a motherfucking JoJo\'s reference??')
        if message.author.id == 386230029169852419:
            await message.channel.send('btw Ghassen, you should watch JoJo\'s')
    if ('You thought it' in message.content) and ('but' in message.content):
        await message.channel.send(file=discord.File(os.path.join('Reacts', 'dio.gif')))

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)
