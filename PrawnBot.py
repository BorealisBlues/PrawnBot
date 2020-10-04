# PrawnBot1.2.2py

import os
import discord
from discord.ext import commands
import random

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

version = '1.2.2'

bot = commands.Bot(command_prefix='!')
#client = discord.Client()

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
            f'{bot.user.name} is connected to the following guild: \n'
            f'{guild.name}(id: {guild.id})'
          )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='version', help='replies with current version')
async def getVersion(ctx):
    print(f'{ctx.author} has issued the getVersion command!')
    await ctx.send(f'my current version is: {version}, thank you for asking! :uwu:')

@bot.command(name='roll', help='simulates rolling dice')
async def roll(ctx, numDnum):
    numDice, numSide = numDnum.split('d')
    numDice = int(numDice)
    numSide = int(numSide)
    print(f'{ctx.author} has issued command roll with {numDnum}')
    dice = [
        str(random.choice(range(1, numSide + 1 )))
        for _ in range(numDice)
        ]
    await ctx.send(', '.join(dice))

@bot.command(name='prawn', help='not yet implimented')
async def prawn(ctx):
    print(f'{ctx.author} has issued the prawn command!')
    await ctx.send(f'I\'m sorry {ctx.author}, but I can\'t bring you any prawn just yet :pensive:') 

bot.run(TOKEN)

# https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python
