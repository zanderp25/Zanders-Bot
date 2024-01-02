import discord, typing, random, asyncio, aiohttp
from datetime import datetime
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.gif_cache = {}
        for channel in [
            1121159013309087794, # wink
            1121159519809048748, # hug
            1121159545624985612, # pat
            1191087790683869204, # slap
            1191090178668888095, # bonk
        ]:
            self.gif_cache[channel] = [msg async for msg in self.bot.get_channel(channel).history(limit=1000)]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.gif_cache.keys():
            self.gif_cache[message.channel.id].append(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id in self.gif_cache.keys():
            self.gif_cache[message.channel.id].remove(message)

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
    async def dice(self, ctx: commands.Context, *, number: typing.Optional[int] = 1, sides: typing.Optional[int] = 6):
        '''
        Roll some dice
        
        Parameters
        ---
        number
            The number of dice to roll
        sides
            How many sides each die should have
        '''
        dice = self.RerollView.dice
        if not 0 < number <= 20: return await ctx.send("You can only roll between 1 and 20 dice!", ephemeral=True)
        if sides < 1: return await ctx.send("An object with less than 1 side just doesn't exist!", ephemeral=True)
        if sides != 6:
            choices = [random.randint(0,sides-1) for _ in range(number)]
            await ctx.send(f"# You rolled: {', '.join([str(choice+1) for choice in choices])}", view=self.RerollView(ctx.author, number, sides))
        elif number == 1:
            choice = random.randint(0,5)
            await ctx.send(f"# {dice[choice]} You rolled a {choice+1}!", view=self.RerollView(ctx.author, 1))
        else:
            choices = [random.randint(0,5) for _ in range(number)]
            await ctx.send(f"{' '.join([dice[choice] for choice in choices])}", view=self.RerollView(ctx.author, number))

    class RerollView(discord.ui.View):
        def __init__(self, author: discord.Member, number: int, sides: int = 6):
            super().__init__()
            self.author = author
            self.number = number
            self.sides = sides
        
        dice = [
            "<:die1:1147923683403378769>",
            "<:die2:1147923685257257062>",
            "<:die3:1147923687274713108>",
            "<:die4:1147923689040523397>",
            "<:die5:1147923696179224586>",
            "<:die6:1147923699505320018>",
        ]

        @discord.ui.button(label="Reroll", style=discord.ButtonStyle.green, emoji="<:reroll:1191524207654355005>")
        async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button,):
            if interaction.user.id != self.author.id:
                return await interaction.response.send_message("You can't reroll someone else's dice!", ephemeral=True)
            if self.sides != 6:
                choices = [random.randint(0,self.sides-1) for _ in range(self.number)]
                await interaction.response.edit_message(content=f"# You rolled: {', '.join([str(choice+1) for choice in choices])}", view=self)
            elif self.number == 1:
                choice = random.randint(0,5)
                await interaction.response.edit_message(content=f"# {self.dice[choice]} You rolled a {choice+1}!", view=self)
            else:
                choices = [random.randint(0,5) for _ in range(self.number)]
                await interaction.response.edit_message(content=f"{' '.join([self.dice[choice] for choice in choices])}", view=self)

    @commands.hybrid_command()
    async def coinflip(self, ctx):
        '''Flip a coin'''
        num = random.randint(1,101)
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

            Parameters
            ---
            user
                The user to wink at. Optional.
        '''
        message_choices = [
            "ehe",
            "✨",
            "*wink wink*",
            "✨😉✨",
            "You have been blessed with a virtual wink!",
            "Behold, the mystical power of a virtual wink!",
        ]

        embed = discord.Embed(title=random.choice(message_choices), color=0x00ff00)
        message = random.choice(self.gif_cache[1121159013309087794])
        if user == ctx.author:
            embed.title = "Why are you winking at yourself?"
        embed.set_image(url=await self.get_gif(message))

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*wink wink* {user.mention}")

    @commands.hybrid_command(name="pat", aliases=["*pats*", "pats", "patpat"])
    async def pat(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Pats someone.

            Parameters
            ---
            user
                The user to pat. Optional.
        '''
        message_choices = [
            "*pat pat*",
            "The digital hand of encouragement has spoken. *pat pat*",
            "When life gives you lemons, pat them. *pat pat*",
            "When you're feeling down, just remember that you're awesome. *pat pat*",
            "Do you like pats? I like pats. *pat pat*",
            "You've been blessed with a virtual pat! *pat pat*",
            "[Everyone liked that.]",
        ]

        embed = discord.Embed(title="*pat pat*", color=0x00ff00)
        message = random.choice(self.gif_cache[1121159545624985612])
        if user == ctx.author:
            embed.title = "*pats you*"
        embed.set_image(url=await self.get_gif(message))

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*pats {user.mention}*")

    @commands.hybrid_command(name="hug", aliases=["*hugs*", "hugs", "bearhug"])
    async def hug(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Hugs someone.

            Parameters
            ---
            user
                The user to hug. Optional.
        '''
        message_choices = [
            "Don't squeeze too hard!",
            "You just got hugged!",
            "Don't forget that you're awesome!",
            "You've been blessed with a virtual hug!",
            "You should hug someone more often.",
            "When you're feeling down, just remember that you're awesome.",
            "When life gives you challenges, a hug can help.",
            "When life gives you lemons, hug them.",
        ]

        embed = discord.Embed(title=random.choice(message_choices), color=0x00ff00)
        message = random.choice(self.gif_cache[1121159519809048748])
        if user == ctx.author:
            embed.title = ("You must be really lonely to hug yourself.")
        embed.set_image(url=await self.get_gif(message))

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*hugs {user.mention}*")

    @commands.hybrid_command(name="slap", aliases=[])
    async def slap(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Slaps someone.

            Parameters
            ---
            user
                The user to slap. Optional.
        '''
        message_choices = [
            "You just got hit with the mighty hand of inconvenience! ✋",
            "The smack heard around the world!",
            "You just got slapped!",
            "Congratulations! You've been visited by the digital palm of surprise! ✋✨",
            "Don't hit too hard!",
            "Consider yourself virtually slapped. Good times.",
            "You've been hit by! You've been struck by! My hand. *slap*",
            "To slap or not to slap, that is the question. And the answer is... *slap*",
            "No one expects the slapping inquisition! *slap*",
            "[Everyone disliked that.]",
            "How about a big ol' slap to the face? *slap*",
        ]

        embed = discord.Embed(title=random.choice(message_choices), color=0x00ff00)
        message = random.choice(self.gif_cache[1191087790683869204])
        if user == ctx.author:
            embed.title = ("Why are you slapping yourself? lol")
        embed.set_image(url=await self.get_gif(message))

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*slaps {user.mention}*")

    @commands.hybrid_command(name="bonk", aliases=["bonks"])
    async def bonk(self, ctx: commands.Context, *, user: discord.Member=None):
        '''
            Bonks someone.

            Parameters
            ---
            user
                The user to bonk. Optional.
        '''
        message_choices = [
            "Bonk! That's the sound of the humor hammer hitting you gently on the noggin. 🔨",
            "You've been hit by! You've been struck by! A smooth criminal! *bonk*",
            "You've been hit by! You've been struck by! A *bonk*",
            "You've been bonked! Time to contemplate your life choices with a gentle tap on the head.",
            "Behold, the gentle bonk of enlightenment has graced your presence. ✨🔨✨",
            "According to the judgement of the Oratrice Mecanique d'Analyse Cardinale, we now turn to the Oratrice Mecanique d'Analyse Cardinale.",
            "Bonk! Your brain has been upgraded to the latest version of puns and silliness, enjoy! 💾🔨" ,
            "You've just experienced a bonk of enlightenment. Welcome to the club of mildly confused wisdom seekers. 🧠🔨",
        ]

        embed = discord.Embed(title=random.choice(message_choices), color=0x00ff00)
        message = random.choice(self.gif_cache[1191090178668888095])
        if user == ctx.author:
            embed.title = ("you look funny bonking yourself lol")
        embed.set_image(url=await self.get_gif(message))

        if user is None:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, content=f"*bonks {user.mention}*")

    async def get_gif(self, message):
        if len(message.attachments) > 0:
            return message.attachments[0].url
        else:
            url = message.content
            if "tenor.com" in url:
                url += ".gif"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        url = str(resp.url)
            return url

async def setup(bot):
    await bot.add_cog(Fun(bot))