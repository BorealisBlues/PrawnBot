# bot.py

import os

import discord

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
            f'{client.user} is connected to the following guild: \n'
            f'{guild.name}(id: {guild.id})'
          )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ('@mr. prawn' in message.content.lower()) or client.user.mentioned_in(message):
        if 'i love you' in message.content.lower():
            print(f'{message.author} has given dobby love <3')
            await message.channel.send('i love you too! :sparkling_heart:')
        else:
            print(f'{message.author} has asked for help')
            responce = (f'How can I help you today {message.author}?')
            await message.channel.send(responce)

client.run(TOKEN)

# https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python
