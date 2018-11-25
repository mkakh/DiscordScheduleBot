import discord
import setting
from discord.ext import commands

TOKEN = setting.token
FILE_NAME = "schedule.dat"
import discord
from discord.ext import commands

PREFIX='$'
bot = commands.Bot(command_prefix=PREFIX)

def set_date(M: int, D:int, h:int, m:int, message:str):
    with open(FILE_NAME, "a") as f:
        f.write("{0:02},{1:02},{2:02},{3:02},{4}".format(M,D,h,m,message))

def permission():
    return True
        
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(a: int, b: int):
    await bot.say(a+b)

@bot.command()
async def multiply(a: int, b: int):
    await bot.say(a*b)

@bot.command()
async def greet():
    await bot.say(":smiley: :wave: Hello, there!")

@bot.command()
async def set(M: int, D:int, h:int, m:int, message:str):
    if (1 <= M and M <= 12):
        if (1 <= M and M <= 31):
            if (0 <= h and h <= 23):
                if (0 <= m and m <= 59):
                    set_date(M,D,h,m,message)
                    await bot.say("{0:02}/{1:02} {2:02}:{3:02}に{4}を設定しました．".format(M,D,h,m,message))

@bot.command()
async def check():
    with open(FILE_NAME, "r") as f:
        raw_date = f.read()
    date = raw_date.split(",")
    await bot.say("{}/{} {}:{}に{}が設定されています．".format(*date))
    
bot.run(TOKEN)
