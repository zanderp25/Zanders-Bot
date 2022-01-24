import discord, typing
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

    @commands.command(aliases=["こんにちは", "hola"])
    async def hello(self, ctx: commands.Context):
        '''Hello to you, too!
        This command is available in these languages:
        en, es, ja'''
        time = datetime.now()
        lang = "ja" if ctx.invoked_with == "こんにちは" else "es" if ctx.invoked_with == "hola" else "en"
        name = ctx.author.display_name
        mention = ctx.author.mention

        if lang == "ja":
            greeting = f"{name}、こんにちは！"
        elif lang == "es":
            greeting = f"¡Hola, {name}!"
        else:
            greeting = f"Hello, {name}!"
        await ctx.send(
            embed = discord.Embed(
                title = "\U0001f44b " + greeting, 
                description = f"_{mention} said hello... Hi!_"
            ).set_footer(text=f"Language: {lang}")
        )
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} said Hello!')

    @commands.command(hidden=True)
    async def apple(self, ctx: commands.Context):
        await ctx.send("\uf8ff")

    @commands.command(aliases=['<:shut:751421349355978822>', "cmp_shut"])
    async def shut(self, ctx: commands.Context):
        '''cmp shut'''
        time = datetime.now()
        await ctx.send(f'<:shut:751421349355978822>')
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author}  said cmp shut')

    @commands.command()
    async def time(self, ctx: commands.Context):
        '''Shows the localtime of the bot (EST) and UTC time.'''
        time = datetime.now()
        utctime = datetime.utcnow()
        await ctx.send(embed = discord.Embed(title = "\u23f0 Times in EST and UTC", description = f'Local Time: `{time}`'+'\n'+f'UTC time: `{utctime}`', color = 0x0000e0))
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} Requested the time')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        '''Test the latency of the bot'''
        time = datetime.now()
        await ctx.send('Pong! `' + str(round(self.bot.latency * 1000)) + ' ms` <a:party_parrot:720424857699090464>')
        await self.log(f'{time} - Pinged by {ctx.author} in {ctx.guild} / #{ctx.channel} | Ponged with {round(self.bot.latency*1000)} ms')

    @commands.command(aliases=['log'])
    async def say(self, ctx: commands.Context, *, arg:str):
        '''Say something to the bot'''
        time = datetime.now()
        embed = discord.Embed(title = f"{ctx.author} said something...", description = f"{arg}", color = 0x0000e0)
        await ctx.channel.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} says "{arg}"')

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, hide:typing.Optional[bool]=False, *, message:str):
        '''Like the shell echo command'''
        if hide:
            await ctx.message.delete()
        await ctx.channel.send(f"{''.join(message)}")

    @commands.command()
    async def avatar(self, ctx: commands.Context, *, member:discord.Member=None):
        '''Gets the avatar of a user'''
        if member is None:
            member = ctx.author
        await ctx.send(
            embed = discord.Embed(
                title = f"{member}'s avatar", 
                color = 0x0000e0
            )
        ).set_image(url = member.avatar.url)

def setup(bot):
    bot.add_cog(Main(bot))
