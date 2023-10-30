import discord, typing, random, asyncio, aiohttp
from datetime import datetime
from discord.ext import commands

class Fun(commands.Cog):
    async def __init__(self, bot):
        self.bot = bot
        await self.load_gif_cache()

    async def load_gif_cache(self):
        self.gif_cache = {}
        for channel in [1121159013309087794, 1121159519809048748, 1121159545624985612]:
            self.gif_cache[channel] = [msg async for msg in self.bot.get_channel(channel).history(limit=1000)]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel in self.gif_cache.keys():
            self.gif_cache[message.channel].append(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel in self.gif_cache.keys():
            self.gif_cache[message.channel].remove(message)

    @commands.hybrid_command(aliases=["pop", "bubble", "bubblewrap"])
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

    @commands.hybrid_command()
    async def dice(self, ctx):
        '''Roll a die'''
        return await ctx.send(f"It's a {random.randint(1,6)}!")

    @commands.hybrid_command()
    async def coinflip(self, ctx):
        '''Flip a coin'''
        num = random.randint(1,100)
        if num == 69:
            return await ctx.send("# <:gasp:923725209821921281> Oh, no! I dropped the coin! Try again.")
        if num % 2:
            return await ctx.send("# <:heads:1147937093897691186> It's heads!")
        else:
            return await ctx.send("# <:tails:1147937095181144154> It's tails!")

    @commands.command(name="-;", aliases=["(","😭"], hidden=True)
    async def waaa(self, ctx):
        '''cry about it'''
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
        if pwp == "¯\_(ツ)_/¯":
            await asyncio.sleep(2)
            await m.edit(content="¯\\\_(.\_.)\_/¯")

    @commands.hybrid_command(name="wink", aliases=[")", "-)"])
    async def wink(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Winks at someone.
            User is optional.
        '''
        if user == ctx.author:
            await ctx.send("Why are you winking at yourself?")
            return
        embed = discord.Embed(title="ehe", color=0x00ff00)
        messages = self.gif_cache[1121159013309087794]
        message = random.choice(messages)
        del messages

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        else:
            url = message.content
            if "tenor.com" in url:
                url += ".gif"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        url = str(resp.url)
            embed.set_image(url=url)

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*wink wink* {user.mention}")

    @commands.hybrid_command(name="pat", aliases=["*pats*", "pats", "patpat"])
    async def pat(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Pats someone.
            User is optional.
        '''
        embed = discord.Embed(title="*pat pat*", color=0x00ff00)
        messages = self.gif_cache[1121159545624985612]
        message = random.choice(messages)
        del messages
        if user == ctx.author:
            embed.title = "*pats you*"

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        else:
            url = message.content
            if "tenor.com" in url:
                url += ".gif"
                print(url)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        url = str(resp.url)
            print(url)
            embed.set_image(url=url)

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*pats {user.mention}*")

    @commands.hybrid_command(name="hug", aliases=["*hugs*", "hugs", "bearhug"])
    async def hug(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Hugs someone.
            User is optional.
        '''
        embed = discord.Embed(title="Don't squeeze too hard!", color=0x00ff00)
        if user == ctx.author:
            embed.title = ("You must be really lonely to hug yourself.")
        messages = self.gif_cache[1121159519809048748]
        message = random.choice(messages)
        del messages

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        else:
            url = message.content
            if "tenor.com" in url:
                url += ".gif"
                print(url)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        url = str(resp.url)
            print(url)
            embed.set_image(url=url)

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*hugs {user.mention}*")

async def setup(bot):
    await bot.add_cog(await Fun(bot))