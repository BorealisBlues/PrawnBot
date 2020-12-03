# PrawnBot.py


import requests
import os
import discord
from discord.ext import commands
import random
import datetime
import asyncio


from dotenv import load_dotenv

#loads environment variables from a .env file in the same directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NSFW_ID = int(os.getenv('NSFW_CHANNEL'))

#defined up top for easy changing
version = '1.4'

#sets command prefix to any character
bot = commands.Bot(command_prefix='!')


#declare an empty dictionary to store reminder values
MedTime = {}


#logCommand logs the command and author to the console
def logCommand(ctx):
    print(f'{ctx.author} has issued the {ctx.command} command!')


#weekdayToNumber takes a string input and returns a value between 0 and 6, as if using datetime.date.weekday()
def weekdayToNumber(day):
    day = day.lower()
    if ((day == 'mon') or (day == 'monday')):
        return 0
    elif ((day == 'tue') or (day =='tuesday')):
        return 1
    elif ((day == 'wed') or (day == 'wednesday')):
        return 2
    elif ((day == 'thu') or (day == 'thursday')):
        return 3
    elif ((day == 'fri') or (day == 'friday')):
        return 4
    elif ((day == 'sat') or (day == 'saturday')):
        return 5
    elif ((day == 'sun') or (day == 'sunday')):
        return 6
    else:
        return 7
        


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


# on_ready prints the connected guilds and members on connection
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
            f'{bot.user.name} is connected to the following guild: \n'
            f'{guild.name}(id: {guild.id})'
          )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
    #reminder loop!
    while True:
        currentHour = datetime.datetime.now().hour
        currentWeekday = datetime.date.weekday(datetime.date.today())
        print(f'current hour is {currentHour} and the day of the week is {currentWeekday}!')
        if ((currentHour,'any') in MedTime):
            print ('found someone to remind!')
            for i in (MedTime[(currentHour,'any')]):
                print(f'reminding {i}!')
                if i.dm_channel is None:
                    print(f'creating a dm channel for {i}!')
                    await i.create_dm()
                print(f'attempting to send a message to {i} through dms!')
                await i.dm_channel.send("Don't foget to take your meds! :shrimp:")
                
        elif ((currentHour,currentWeekday) in MedTime):
            print ('found someone to remind!')
            for i in (MedTime[(currentHour,currentWeekday)]):
                print(f'reminding {i}!')
                if i.dm_channel is None:
                    print(f'creating a dm channel for {i}!')
                    
                    await i.create_dm()
                print(f'attempting to send a message to {i} through dms!')
                await i.dm_channel.send("Don't foget to take your meds! :shrimp:")
        print('waiting for next loop!')
        await asyncio.sleep(3600)
    


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
@bot.command(name='prawn', help='delivers prawn')
async def prawn(ctx):
    logCommand(ctx)
    if (ctx.channel.id == NSFW_ID):
        r = requests.get('https://pornhub.com/video/random') #sends a request to pornhub's random function
        #this redirects twice, first to the actual server with the random function, then to the video requested
        await ctx.send(f'Here you go {ctx.author}! the prawn you asked for! :innocent: ||https://pornhub.com{r.history[1].headers["location"]}||')
    else:
        await ctx.send(f'I\'m sorry {ctx.author}, but I can\'t put prawn anywhere but your NSFW channel :pensive:')


# the !brick command replies with a brick pick
@bot.command(name='brick',help='sends a brick pic')
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

#the !ily command validates people
@bot.command(name='ily',help='I love you too!')
async def ily(ctx):
    logCommand(ctx)
    await ctx.send('I love you too! :smiling_face_with_3_hearts:')


#The !remindme command adds a user to a list to be reminded to do things
@bot.command(name='remindme',help="I'll remind you to take your meds! please note that I assume AM unles you say Pm!")
async def reminddme(ctx, time, day='any'):
    logCommand(ctx)
    await ctx.send(f'Okay, i\'ll remind you at {time}')
    if ('pm' in time.lower()):
        time = (int(time.replace('pm','')) + 12)
    else:
        time = int(time.replace('am',''))
    if (day != 'any'):
        daytemp = weekdayToNumber(day)
        day = daytemp
    if (day == 7):
        await ctx.send(f"I'm sorry {ctx.author}, but I don't know what day of the week that is :pensive:")
    if (day != 7):
        if ((time,day) not in MedTime):
            MedTime[(time,day)] = []
        MedTime[(time,day)].append(ctx.author)
    print (MedTime)


    
bot.run(TOKEN)
