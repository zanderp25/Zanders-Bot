import discord
from datetime import datetime
from discord.ext import commands
from jishaku.codeblocks import Codeblock, codeblock_converter


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()
    
    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, command):
        time = datetime.now()
        embed = discord.Embed(title=f"Enabled `;{command}``", color=0x06c706)
        ctx.bot.get_command(command).update(enabled=True)
        await ctx.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} enable `;{command}`')

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, command):
        time = datetime.now()
        embed = discord.Embed(title=f"Disabled `;{command}`", color=0xd10606)
        ctx.bot.get_command(command).update(enabled=False)
        await ctx.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} disabled `;{command}`')

    @commands.command()
    @commands.is_owner()
    async def eval(self,ctx, *, argument:codeblock_converter):
        await self.bot.cogs["Jishaku"].jsk_python(ctx=ctx,argument=argument)

def setup(bot):
    bot.add_cog(Dev(bot))