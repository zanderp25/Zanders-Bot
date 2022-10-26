import discord
from datetime import datetime
from discord.ext import commands
import os
import ffmpeg
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()

    @commands.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
    @commands.is_owner()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"Joined {channel}")
    
    @commands.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
    @commands.is_owner()
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music end or use the 'stop' command")
            return
        await ctx.send("Getting everything ready, playing audio soon")
        print("Someone wants to play music let me get that ready for them...")
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

    @commands.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
    @commands.is_owner()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left {channel}")
        else:
            await ctx.send("Don't think I am in a voice channel")
        
async def setup(bot):
    await bot.add_cog(Music(bot))