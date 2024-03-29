#Made by Zanderp25#1897
import discord
from discord.ext import commands
import datetime
import sys, os, DPyUtils

import ffmpeg
from discord import FFmpegPCMAudio
import youtube_dl

import dotenv
dotenv.load_dotenv(verbose=True)

token = open("token.txt").read()
intents = discord.Intents.all()
owner_ids = {511655498676699136,642416218967375882,1078147341141409843}
bot = commands.Bot(command_prefix=commands.when_mentioned_or(';','；'), intents=intents, case_insensitive=True, owner_ids=owner_ids)

cogs = ['jishaku', 'DPyUtils.ContextEditor2']

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        cogs.append(f"cogs.{file[:-3]}")

# for cog in cogs:
#     try:
#         bot.load_extension(cog)
#     except Exception as error:
#         print(error)
#bot.load_extension('riftgun')

def log(x):
    print(x)
    f = open("bot.log", 'a')
    f.write('\n' + x)
    f.close()

@bot.event
async def on_ready():
    for cog in cogs:
        try:
            await bot.load_extension(cog)
        except Exception as error:
            print(error)
    # bot.msg_del_emoji = '<:major_outage:803672907724226621>'
    time = datetime.datetime.now()
    log(f'{time} - Bot is logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if (str(message.content) == ';Nice') | (str(message.content) == ';nice'):
        time = datetime.datetime.now()
        await message.channel.send(f'Nice')
        if str(message.author) == 'Zanderp25#1897':
            nice = '(Nice)'
        else:
            nice = ''
        log(f'{time} - {message.guild} / #{message.channel} - Nice - {message.author} {nice}')
        
    if message.content.startswith('GG') & (str(message.author)=='MEE6#4876'):
        time = datetime.datetime.now()
        await message.channel.send(f'Stop it, {message.author.mention}')
        log(f'{time} - Dad, {message.author} is being annoying againn.. ({message.guild} / #{message.channel})')
    
    await bot.process_commands(message)

bot.run(token)
