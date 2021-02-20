import discord, os
from datetime import datetime
from discord.ext import commands
from jishaku.codeblocks import Codeblock

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()

    @commands.group(aliases=["minecraft"])
    @commands.is_owner()
    async def mc(self, ctx):
        '''Controls the Minecraft server'''
        pass

    @mc.command(name="start")
    async def mc_start(self, ctx):
        '''Starts the Minecraft server'''
        m = await ctx.send("<a:loading:742718904622907463> Starting server...")
        os.system('echo "pm2 start 0" | ssh 192.168.0.11')
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
        os.system('echo "pm2 stop 0" | ssh 192.168.0.11')
        await m.edit(content="Server stopped!")

    @mc.command(name="backup")
    async def mc_backup(self, ctx):
        '''Saves a backup of the server'''
        m = await ctx.send("<a:loading:742718904622907463> Stopping server...")
        os.system('echo "pm2 stop 0" | ssh 192.168.0.11')
        await m.edit(content="<a:loading:742718904622907463> Backing up the server...")
        os.system('echo "cd ~/Minecraft; ./backup.sh" | ssh 192.168.0.11')
        await m.edit(content="<a:loading:742718904622907463> Starting server...")
        os.system('echo "pm2 start 0" | ssh 192.168.0.11')
        await m.edit(content="Done!")
    
    @mc.command(name="log")
    async def mc_log(self,ctx):
        '''View the log of the Minecraft Server'''
        await self.bot.cogs["Jishaku"].jsk_shell(ctx=ctx, argument=Codeblock("", 'echo "pm2 log 0" | ssh 192.168.0.11'))

    @commands.command(aliases = ["requestvc","vc"])
    async def personalvc(self, ctx):
        if ctx.guild.id == 611278159555461180:
            if ctx.channel.id == 755948130356297768:
                try:
                    ch = ctx.guild.get_channel(751903455106433184)
                    for channel in ch.channels:
                        if channel.name == str(ctx.author):
                            await ctx.send(embed=discord.Embed(name=ctx.author, title="Voice Channel Exists", description="You already have a voice channel! Why would you want another?", color=discord.Color.red()))
                            return
                    await ch.create_voice_channel(name=str(ctx.author), overwrites={ctx.author:discord.PermissionOverwrite(view_channel=True, connect=True), ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False, connect=False)})
                    await ctx.send(embed=discord.Embed(name=ctx.author, title="Voice Channel Created", description="You now have a voice channel of your own. :) Good luck finding it lol", color=discord.Color.green()))
                except Exception as e:
                    await ctx.send(embed=discord.Embed(title="Error", description=f"An error occured.```{e}```", color=discord.Color.red()))
            else:
                await ctx.send("Try in <#755948130356297768>")

def setup(bot):
    bot.add_cog(Main(bot))
