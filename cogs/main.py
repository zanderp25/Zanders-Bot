import discord
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

    @commands.command()
    async def hello(self, ctx):
        '''Hello to you, too!'''
        time = datetime.now()
        await ctx.send(embed = discord.Embed(title = "\U0001f44b" + f" Hello, {ctx.author}!", description = f"_{ctx.author.mention} said hello... Hi!_"))
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} said Hello!')

    @commands.command(aliases=['<:shut:751421349355978822>', "cmp_shut"])
    async def shut(self, ctx):
        '''cmp shut'''
        time = datetime.now()
        await ctx.send(f'<:shut:751421349355978822>')
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author}  said cmp shut')

    @commands.command()
    async def time(self, ctx):
        '''Shows the localtime of the bot (EST) and UTC time.'''
        time = datetime.now()
        utctime = datetime.utcnow()
        await ctx.send(embed = discord.Embed(title = "\u23f0 Times in EST and UTC", description = f'Local Time: `{time}`'+'\n'+f'UTC time: `{utctime}`', color = 0x0000e0))
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} Requested the time')

    @commands.command()
    async def ping(self, ctx):
        '''Test the latency of the bot'''
        time = datetime.now()
        await ctx.channel.send('Pong! `' + str(round(self.bot.latency * 1000)) + ' ms` <a:party_parrot:720424857699090464>')
        await self.log(f'{time} - Pinged by {ctx.author} in {ctx.guild} / #{ctx.channel} | Ponged with {round(self.bot.latency*1000)} ms')

    @commands.command(aliases=['log'])
    async def say(self, ctx, *, arg:str):
        '''Say something to the bot'''
        time = datetime.now()
        embed = discord.Embed(title = f"{ctx.author} said something...", description = f"{arg}", color = 0x0000e0)
        await ctx.channel.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} says "{arg}"')

    @commands.command(hidden=True)
    async def secret(self, ctx):
        '''Uhh... you're not supposed to see this
        
        Well... I guess you see it now... This is a command that provides a link to a website that has a 1 in 50 chance to reveal a secret.
        ||Maybe something else, too.||'''
        time = datetime.now()
        await ctx.channel.send(embed = discord.Embed(title = "1 in 50 Chance", description = f'[Reveal Secret](https://zanderp25.com/secret)'))
        await ctx.message.delete()
        await self.log(f'{time} - {ctx.author} got Rick-Rolled in {ctx.guild} / #{ctx.channel}')

def setup(bot):
    bot.add_cog(Main(bot))