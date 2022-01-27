import discord, os, re
from datetime import datetime
from discord.ext import commands
from jishaku.codeblocks import Codeblock
import functools

class NotInGuild(commands.CheckFailure): 
    '''Exception raised when :func:`@is_in_guild` fails.'''
    def __init__(self, message):
        super().__init__(message)

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_in_guild(guild):
        """A :func:`commands.check` that checks if the person invoking this command is the
        owner of the bot.

        This check raises a special exception, :exc:`.NotInGuild` that is derived
        from :exc:`commands.CheckFailure`.
        """

        async def predicate(ctx):
            if not ctx.guild.id == guild:
                raise NotInGuild('You are not in the guild.')
            return True

        return commands.check(predicate)

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()
        
    async def run_sync(self, func: callable, *args, **kwargs):
        return await self.bot.loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    @commands.group(aliases=["minecraft"])
    @commands.is_owner()
    async def mc(self, ctx):
        '''Controls the Minecraft server'''
        pass

    @mc.command(name="start")
    async def mc_start(self, ctx):
        '''Starts the Minecraft server'''
        m = await ctx.send("<a:loading:742718904622907463> Starting server...")
        await self.run_sync(os.system, 'pm2 start 1')
        await m.edit(content="Server started!")

    @mc.command(name="stop")
    async def mc_stop(self, ctx):
        '''Stops the Minecraft server'''
        m = await ctx.send("<a:loading:742718904622907463> Stopping server...")
        await self.bot.get_guild(611278159555461180).get_channel(787729896709029889).send("stop")
        await m.edit(content="Server stopped!")

    @mc.command(name="force_stop", aliases=["kill","force-stop"])
    async def mc_force_stop(self, ctx):
        '''Kills the Minecraft server'''
        m = await ctx.send("<a:loading:742718904622907463> Stopping server...")
        await self.run_sync(os.system, 'pm2 stop 1')
        await m.edit(content="Server stopped!")

    @mc.command(name="backup")
    async def mc_backup(self, ctx):
        '''Saves a backup of the server'''
        m = await ctx.send("<a:loading:742718904622907463> Stopping server...")
        await self.run_sync(os.system, 'pm2 stop 1')
        await m.edit(content="<a:loading:742718904622907463> Backing up the server...")
        await self.run_sync(os.system, 'cd ~/Minecraft; ./backup.sh')
        await m.edit(content="<a:loading:742718904622907463> Starting server...")
        await self.run_sync(os.system, 'pm2 start 1')
        await m.edit(content="Done!")

    @mc.command(name="status", hidden=True)
    async def mc_status(self,ctx):
        '''Shows the status of the server'''
        pass
    
    @mc.command(name="log")
    async def mc_log(self,ctx):
        '''View the log of the Minecraft Server'''
        await self.bot.cogs["Jishaku"].jsk_shell(ctx=ctx, argument=Codeblock("", 'pm2 log 1'))

    @commands.command(aliases = ["requestvc","vc"])
    @is_in_guild(611278159555461180)
    async def personalvc(self, ctx):
        if ctx.channel.id == 755948130356297768:
            ch = ctx.guild.get_channel(751903455106433184)
            for channel in ch.channels:
                if channel.name == str(ctx.author):
                    await ctx.send(embed=discord.Embed(name=ctx.author, title="Voice Channel Exists", description="You already have a voice channel! Why would you want another?", color=discord.Color.red()))
                    return
            await ch.create_voice_channel(name=str(ctx.author), overwrites={ctx.author:discord.PermissionOverwrite(view_channel=True, connect=True), ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False, connect=False)})
            await ctx.send(embed=discord.Embed(name=ctx.author, title="Voice Channel Created", description="You now have a voice channel of your own. :) Good luck finding it lol", color=discord.Color.green()))
        else:
            await ctx.send("Try in <#755948130356297768>")

def setup(bot):
    bot.add_cog(Guild(bot))
