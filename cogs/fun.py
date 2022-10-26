import discord, typing, random, asyncio, aiohttp
from datetime import datetime
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pop", "bubble", "bubblewrap"])
    async def bubbles(self, ctx, width:int, height:int):
        '''
            Shows you virtual bubble wrap with a given width and height.
            Made by Clari (💜Clari#7744)

            How to use:
                `;bubbles <width> <height>`
        '''
        width = width if 0<width<=10 else 10
        height = height if 0<height <=20 else 20
        await ctx.send((('||pop||'*width)+'\n')*height)

    @commands.command(name="-;", aliases=["(","😭"], hidden=True)
    async def waaa(self, ctx):
        pwp = [
            ";-;",
            "waaaaa",
            "pwp",
            "owo",
            "*quietly judges you*",
            "There, there...", 
            "._.",
            "¯\_(ツ)_/¯",
        ]
        pwp = random.choice(pwp)
        m = await ctx.send(pwp)
        if pwp is "¯\_(ツ)_/¯":
            await asyncio.sleep(2)
            await m.edit(content="¯\\\_(.\_.)\_/¯")

    @commands.command(name="wink", aliases=[")", "-)"])
    async def wink(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Winks at a user.
            User is optional.
        '''
        embed = discord.Embed(title="ehe", color=0x00ff00)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/wink") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"{user.mention}")

    @commands.command(name="pat", aliases=["*pats*", "pats", "patpat"])
    async def pat(self, ctx: commands.Context, user: discord.Member=None):
        '''
            Pats a user.
        '''
        embed = discord.Embed(title="*pat pat*", color=0x00ff00)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
        await ctx.send(embed=embed, content=f"{user.mention}")

    @commands.command(name="hug", aliases=["*hugs*", "hugs", "bearhug"])
    async def hug(self, ctx: commands.Context, user: discord.Member=None):
        '''
            Hugs a user.
        '''
        if user == ctx.author:
            await ctx.send(random.choice())
            return
        embed = discord.Embed(title="Don't squeeze too hard!", color=0x00ff00)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                embed.set_image(url=data["link"])
        await ctx.send(embed=embed, content=f"{user.mention}")

async def setup(bot):
    await bot.add_cog(Fun(bot))