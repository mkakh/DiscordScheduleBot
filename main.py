# coding: utf-8
import discord
from discord.ext import commands
import setting

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

def com_bash(message):
    message.content = receive_message('bash', message.content)
    message.content = "'" + message.content + "'"
    import subprocess, shlex
    args =  shlex.split(message.content)
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    msg = stdout_data.decode('utf-8') + stderr_data.decode('utf-8')
    return msg

async def com_vote_start(message):
    ids = []
    for msg in ['月', '火', '水', '木', '金', '土', '日']:
        new_message = await client.send_message(message.channel, msg)
        await client.add_reaction(new_message, emoji='👍')
        ids = ids + [new_message.id]
    with open('vote.dat', "w") as f:
        f.write("{}".format(','.join(ids)))

async def com_vote_end(message):
    with open('vote.dat', "r") as f:
        ids = f.read().split(",")
    strs = ['月', '火', '水', '木', '金', '土', '日']
    msg = ''
    for i in range(len(strs)):
        get_message = await client.get_message(message.channel, ids[i])
        votes = sum({react.emoji : react.count for react in get_message.reactions}.values())-1
        msg = msg + strs[i] + ': ' + str(votes) + '\n'
    return msg

def com_help(message):
    return "**一般権限**\nhello: 挨拶\ncheck: 日程確認\nhelp: ヘルプ\n\n**管理者権限**\nset: 日程セット\nbash: Bash\nvote_start: 曜日投票開始\nvote_end: 曜日投票集計"
    

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if not permitted(message.author):
        print('PERMISSION_DENIED: {}'.format(message.content))
        return

    if message.content.startswith(PREFIX):
        message.content = receive_message(PREFIX, message.content)
        if message.content.startswith('hello'):
            msg = com_hello(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('check'):
            msg = com_check(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('help'):
            msg = com_help(message)
            await client.send_message(message.channel, msg)
        elif permitted(message.author):
            if message.content.startswith('set'):
                msg = com_set(message)
                await client.send_message(message.channel, msg)
            elif message.content.startswith('bash'):
                msg = com_bash(message)
                await client.send_message(message.channel, msg)
            elif message.content.startswith('vote_start'):
                await com_vote_start(message)
            elif message.content.startswith('vote_end'):
                msg = await com_vote_end(message)
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, "？？？")
        else:
            await client.send_message(message.channel, "？？？")
                



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
