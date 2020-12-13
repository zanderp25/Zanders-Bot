import discord
import asyncio
from datetime import datetime
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()

    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,reason="No reason given."):
        '''Kicks a user'''
        if "yeet" in ctx.message.content:
            msg = await ctx.send(f"Yeeting member `{member}`")
            await member.kick(reason=reason)
            try:
                await member.send(f"You have been kicked from {ctx.guild} for {reason}")
            except: pass
            await msg.edit(content=f"Succesfully yeeted. ***Y E E T !***")
        else:
            msg = await ctx.send(f"Kicking member `{member}`")
            await member.kick(reason=reason)
            try:
                await member.send(f"You have been kicked from {ctx.guild} for {reason}")
            except: pass
            await msg.edit(content=f"Succesfully kicked.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *,reason="No reason given."):
        '''Bans a user'''
        msg = await ctx.send(f"Banning member `{member}`")
        await member.ban(reason=reason)
        try:
            await member.send(f"You have been banned from {ctx.guild} for {reason}")
        except: pass
        await msg.edit(content=f"Succesfully banned.")

    @commands.command()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int="0", channel: discord.TextChannel="current"):
        """Changes the slowmode of a channel in seconds, using 0 or leaving it blank to reset."""
        if channel == "current":
            async with ctx.typing():
                await ctx.message.channel.edit(slowmode_delay=time, reason=f"Slowmode command called by {ctx.author}")
                await ctx.send(f"Slowmode changed to **{time}** seconds.")
        else:
            async with ctx.typing():
                await channel.edit(slowmode_delay=time, reason=f"Slowmode command called by {ctx.author}")
                await ctx.send(f"Slowmode changed to **{time}** seconds in <#{channel.id}>.")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number:int, purge_pinned_messages:bool = False):
        '''Purges {number} amount of messages. If {purge_pinned_messages} is true, then it will delete pinned messages too.'''
        await ctx.message.delete()
        if purge_pinned_messages == True
            n = await ctx.channel.purge(limit=number)
        else:
            n = await ctx.channel.purge(limit=number, check=!message.pinned)
        msg = await ctx.send(f"Deleted {len(n)} messages.")
        await asyncio.sleep(2)
        await msg.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
