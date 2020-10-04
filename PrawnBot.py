# PrawnBot1.2.py

import os
import discord
from discord.ext import commands
import random

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

version = '1.2'

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

@bot.command(name='list', help='replies with a list of commands, depreciated lmao')
async def getList(ctx):
    commandlist = ['list','version']
    print(f'{ctx.author} has issued the getList command!')
    await ctx.send(f'prefix commands with a \'!\' , my current commands are: {commandlist}')

@bot.command(name='version', help='replies with current version')
async def getVersion(ctx):
    print(f'{ctx.author} has issued the getVersion command!')
    await ctx.send(f'my current version is: {version}')

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

bot.run(TOKEN)

# https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python
