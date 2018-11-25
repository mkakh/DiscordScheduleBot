# coding: utf-8
import discord
import setting
from discord.ext import commands

TOKEN = setting.token
PREFIX='$'
FILE_NAME = 'schedule.dat'

client = discord.Client()

def receive_message(prefix, message):
    if not message.startswith(prefix):
        return message
    message = message[len(prefix):]
    return receive_message(' ', message)

def write_schedule(M: int, D:int, h:int, m:int, message:str):
    # 現在，上書きをしている．追記にして複数予定に対応したい．
    if (1 <= M and M <= 12):
        if (1 <= M and M <= 31):
            if (0 <= h and h <= 23):
                if (0 <= m and m <= 59):
                    with open(FILE_NAME, "w") as f:
                        f.write("{0:02},{1:02},{2:02},{3:02},{4}".format(M,D,h,m,message))

def permitted(user : discord.member.Member):
    allow_users = ['mkakh#3874']
    user = "{}".format(user)
    return (user in allow_users)

def set_date(M: int, D:int, h:int, m:int, message:str):
    with open(FILE_NAME, "a") as f:
        f.write("{0:02},{1:02},{2:02},{3:02},{4}".format(M,D,h,m,message))

def com_hello(message):
    msg = "{0.author.mention} :wave: Hello!".format(message)
    return msg

def com_set(message):
    message.content = receive_message('set', message.content).split(' ')
    sch_content = message.content[4]
    MDhm = list(map(int, message.content[:-1]))
    write_schedule(*MDhm, sch_content)
    msg = '{0.author.mention} {1[0]:02}/{1[1]:02} {1[2]:02}:{1[3]:02}に{2}が設定されました．'.format(message, MDhm, sch_content)
    return msg

def com_check(message):
    with open(FILE_NAME, "r") as f:
        raw_date = f.read()
    date = raw_date.split(",")
    msg = "{}/{} {}:{}に{}が設定されています．".format(*date)
    return msg

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if not permitted(message.author):
        print('PERMISSION_ERROR: {}'.format(message.author))
        return

    if message.content.startswith(PREFIX):
        message.content = receive_message(PREFIX, message.content)
        if message.content.startswith('hello'):
            msg = com_hello(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('set'):
            msg = com_set(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('check'):
            msg = com_check(message)
            await client.send_message(message.channel, msg)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
