# Work with Python 3.6
import discord
import random
import os

TOKEN = #enter bot token here

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # Simple welcome message
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}. How can Mecha Senku assist you today?'.format(message)
        await message.channel.send(msg)
    # Dice roll function
    if message.content.startswith('!dice'):
        dice = random.randint(1, 6)
        filename = "dice " + str(dice) + ".png"
        dicename = os.path.join('dice', filename)
        await message.channel.send('You rolled ' + str(dice), file=discord.File(dicename))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)