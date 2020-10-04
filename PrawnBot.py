# PrawnBot1.3.1py


import requests
import os
import discord
from discord.ext import commands
import random


from dotenv import load_dotenv

#loads environment variables from a .env file in the same directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#defined up top for easy changing
version = '1.3.1'

#sets command prefix to any character
bot = commands.Bot(command_prefix='!')


#logCommand logs the command and author to the console
def logCommand(ctx):
    print(f'{ctx.author} has issued the {ctx.command} command!')


# getNameDict takes a nametype, pulls javascript from fantasynamegenerators, and returns the namelists as a dictionary, returns status code on error
def getNameDict(NameType):
    r = requests.get(f'https://www.fantasynamegenerators.com/scripts/dnd{NameType}Names.js')
    print(f'status code: {r.status_code}')
    if (r.status_code == 200):
        i = 0
        namedict = {}
        while (i < 4):
            i += 1
            nmPos1 = r.text.find(f"var nm{i}")
            print(f'namelist{i} found starting at pos {nmPos1}')
            nmPos2 = r.text.find(';', nmPos1)
            print(f'namelist{i} found ending at pos {nmPos2}, character: {r.text[nmPos2]}')
            listInProgress = r.text[nmPos1:nmPos2].translate({ord(i): None for i in '[]; ="'})
            listInProgress = listInProgress.replace(f'varnm{i}','')
            listInProgress = listInProgress.strip('\n')
            listInProgress = listInProgress.split(',')
            print(f'name list {i}: {listInProgress}')
            namedict["nameList{0}".format(i)] = listInProgress
        return namedict
    else:
        print(f'status code: {r.status_code}')
        return r.status_code

#saves typing
def getRandom(namelist):
    return str(random.choice(namelist))


#takes the name dictionary and a nametype, returns names
def nameGen(nameDict, nametype):
    if (nametype.lower() == 'masc'):
        return (getRandom(nameDict['nameList1'])+getRandom(nameDict['nameList2']) + ' ' + (getRandom(nameDict['nameList1'])+getRandom(nameDict['nameList2'])))
    elif (nametype.lower() == 'fem'):
        return (getRandom(nameDict['nameList3'])+getRandom(nameDict['nameList4']) + ' ' + (getRandom(nameDict['nameList3'])+getRandom(nameDict['nameList4'])))
    elif (nametype.lower() == 'neutral'):
        return (getRandom(nameDict['nameList1'])+getRandom(nameDict['nameList4']) + ' ' + (getRandom(nameDict['nameList3'])+getRandom(nameDict['nameList2'])))
    else:
        return (getRandom(nameDict[f'nameList{random.choice(range(1,5))}'])+getRandom(nameDict[f'nameList{random.choice(range(1,5))}']) + ' ' + (getRandom(nameDict[f'nameList{random.choice(range(1,5))}'])+getRandom(nameDict[f'nameList{random.choice(range(1,5))}'])))


# on_ready prints the connectedd guilds and members on connection
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
            f'{bot.user.name} is connected to the following guild: \n'
            f'{guild.name}(id: {guild.id})'
          )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


# the !version command replies with the current version
@bot.command(name='version', help='replies with current version')
async def getVersion(ctx):
    logCommand(ctx)
    await ctx.send(f'my current version is: {version}, thank you for asking! :relaxed:')

    
#the !roll command simulates rolling dice
@bot.command(name='roll', help='simulates rolling dice')
async def roll(ctx, numDnum):
    numDice, numSide = numDnum.split('d')
    numDice = int(numDice)
    numSide = int(numSide)
    logCommand(ctx)
    dice = [
        str(random.choice(range(1, numSide + 1 )))
        for _ in range(numDice)
        ]
    await ctx.send(', '.join(dice))

    
# the !prawn command will, someday, post prawn
@bot.command(name='prawn', help='not yet implimented')
async def prawn(ctx):
    logCommand(ctx)
    await ctx.send(f'I\'m sorry {ctx.author}, but I can\'t bring you any prawn just yet :pensive:')


# the !brick command replies with a brick pick
@bot.command(name='brick',help='sends a pic of a brick, for testing')
async def brick(ctx):
    logCommand(ctx)
    imgUrl = 'https://kingfisher.scene7.com/is/image/Kingfisher/5055013400359_01c'
    await ctx.send(f'Here\'s that brick pic! {imgUrl}')


#the !namegen command takes a nametype argument and returns names from fantasynamegenerator.com
@bot.command(name='namegen',help='generates a name for you! tested inputs include Dwarf, Elf, Halfelf, Halfling! include masc, fem, or neutral to set a preference!')
async def name(ctx, NameType, nameGender='random'):
    logCommand(ctx)
    nameDict = getNameDict(NameType)
    Name = nameGen(nameDict, nameGender)
    await ctx.send(f'I\'ve made a {nameGender} {NameType} name for you! "{Name}"') 

@bot.command(name='ily',help='I love you too!')
async def ily(ctx):
    logCommand(ctx)
    await ctx.send('I love you too! :smiling_face_with_3_hearts:')

bot.run(TOKEN)
