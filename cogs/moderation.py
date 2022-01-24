import discord
import asyncio, typing
from discord.ext import commands

class MemberIsInGuild(commands.BadArgument):
    def __init__(self, message: typing.Optional[str] = None, *args: typing.Any) -> None:
        super().__init__(message, *args)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()

    async def check_hierarchy(
        self,
        ctx: commands.Context,
        obj: typing.Union[discord.Member, discord.Role],
        *,
        return_bool: bool = False,
    ):
        def err(thing):
            if return_bool:
                return False
            raise commands.CheckFailure(f"{obj} is higher than {thing}!")

        if ctx.guild.me.top_role <= getattr(obj, "top_role", obj):
            return err("me")
        if ctx.author.top_role <= getattr(obj, "top_role", obj):
            return err("you")
        return True

    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,reason="No reason given."):
        '''Kicks a user'''
        if await self.check_hierarchy(ctx, member, return_bool=True):
            async def _kick(member):
                await member.kick(reason=reason)
                try:
                    await member.send(f"You have been kicked from {ctx.guild} for {reason}")
                except: pass
            if ctx.invoked_with == "yeet":
                msg = await ctx.send(f"Yeeting member `{member}`")
                await _kick(member)
                return await msg.edit(content=f"Succesfully yeeted. ***Y E E T !***")
            msg = await ctx.send(f"Kicking member `{member}`")
            await _kick(member)
            await msg.edit(content=f"Succesfully kicked.")
        else:
            await ctx.send("You can't do that!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *,reason="No reason given."):
        '''Bans a user'''
        if await self.check_hierarchy(ctx, member, return_bool=True):
            msg = await ctx.send(f"Banning member `{member}`")
            await member.ban(reason=reason)
            try:
                await member.send(f"You have been banned from {ctx.guild} for {reason}")
            except: pass
            await msg.edit(content=f"Succesfully banned.")
        else:
            await ctx.send("You can't do that!")

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
        if purge_pinned_messages == True:
            n = await ctx.channel.purge(limit=number)
        else:
            n = await ctx.channel.purge(limit=number, check=lambda msg: not msg.pinned)
        msg = await ctx.send(f"Deleted {len(n)} messages.")
        await asyncio.sleep(2)
        await msg.delete()
    
    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purgefrom(self, ctx, id:discord.Message):
        '''Purges messages after the specified message, with a limit of 500'''
        await ctx.message.delete()
        n = await ctx.channel.purge(after=id)
        msg = await ctx.send(f"Deleted {len(n)} messages.")
        await asyncio.sleep(2)
        await msg.delete()

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user:discord.User, *,reason="No reason given."):
        '''Unbans a user'''
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"Unbanned {user}")

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user:discord.User, *,reason="No reason given."):
        '''Bans a user that is not in the server'''
        if user.id in [x.id for x in ctx.guild.members]:
            raise MemberIsInGuild("That user is in the server!")
        else:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Banned {user}")

def setup(bot):
    bot.add_cog(Moderation(bot))
