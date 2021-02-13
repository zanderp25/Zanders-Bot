import discord, os
from datetime import datetime
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()

    @commands.command(aliases = ["startmc","stopmc"])
    @commands.is_owner
    async def controlmc(self, ctx):
        if ctx.invoked_with == "startmc":
            m = await ctx.send("<a:loading:742718904622907463> Starting server...")
            os.system("pm2 start 0 | ssh 192.168.0.11")
            await m.edit(content="Server started!")
        elif ctx.invoked_with == "stopmc":
            m = await ctx.send("<a:loading:742718904622907463> Stopping server...")
            os.system("pm2 stop 0 | ssh 192.168.0.11")
            await m.edit(content="Server stopped!")
        else:
            await ctx.send(f"To start/stop the server, do `{ctx.prefix}startmc` or `{ctx.prefix}stopmc`")

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
