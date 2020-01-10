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

token = os.environ['token']

client = discord.Client()

@client.event
async def on_message(message):

    # Confusion message
    if message.content == 'nani' or message.content =='what the fuck' or message.content == 'nani ga fakku':
        await message.channel.send(message.content)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)