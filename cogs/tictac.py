import discord
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    async def tictac(self, ctx, arg):
        '''Unused command, does nothing'''
        pass

def setup(bot):
    bot.add_cog(Main(bot))