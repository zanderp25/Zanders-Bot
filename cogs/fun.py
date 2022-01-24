import discord, re, typing, random, asyncio
from datetime import datetime
from discord.ext import commands

class SquareDraw(commands.Converter):
  async def convert(self, ctx, arg):
    arg = str(arg)
    ks = "kwrboygpn;"
    squares = dict(zip(ks, "⬛⬜🟥🟦🟧🟨🟩🟪🟫\n"))
    sec = rf"([{ks}])(\d+)?"
    primreg = re.compile(rf"\((\d+)x(({sec})+)\)", flags=re.IGNORECASE |re.MULTILINE)
    while (it:=list(primreg.finditer(arg))):
      for m in it:
        print(arg)
        arg=arg.replace(m.group(0), m.group(2)*int(m.group(1)))
    reg = re.compile(sec, flags=re.IGNORECASE|re.MULTILINE)
    matches = reg.finditer(arg)
    if not matches:
        return "blank"
    line = ""
    for m in matches:
        print(arg)
        k, n = m.groups();n=n or 1
        line += squares[k.lower()] * int(n)
    return line


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sd", "sq", "square", "draw"])
    async def squaredraw(self, ctx, *lines: SquareDraw):
        '''
            Draws an image with emoji squares.
            Made by Clari (💜Clari#7744)

            How to use:
                Use a letter below to represent the color of each square, and a number following the letter
                to represent the number of squares of that color. The number of squares is optional.
                (Space also works as a line separator.)
                Example:
                    `k2r3k2`
                You can also use groups, like this:
                    `(3x(k2r3k2;))`

            Colors:
                - k - black
                - w - white
                - r - red
                - b - blue
                - o - orange
                - y - yellow
                - g - green
                - p - purple
                - n - brown
                - ; - newline             
            
            Example:
                `;squaredraw (4x(4xkw);(4xwk);)`
        '''
        return await ctx.send(embed=discord.Embed(title='Here\'s your monster', description='\n'.join(lines)))

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
        await ctx.send((('pop'*width)+'\n')*height)

    @commands.command(name="-;", aliases=["(","😭"], hidden=True)
    async def waaa(self, ctx, e:typing.Optional[bool]=False):
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

    @commands.command(hidden=True, disabled=True)
    async def secret(self, ctx):
        '''Uhh... you're not supposed to see this
        
        Well... I guess you see it now... This is a command that provides a link to a website that has a 1 in 50 chance to reveal a secret.
        ||Maybe something else, too.||'''
        time = datetime.now()
        await ctx.channel.send(embed = discord.Embed(title = "1 in 50 Chance", description = f'[Reveal Secret](https://zanderp25.com/secret)'))
        await ctx.message.delete()
        await self.log(f'{time} - {ctx.author} got Rick-Rolled in {ctx.guild} / #{ctx.channel}')

def setup(bot):
    bot.add_cog(Fun(bot))