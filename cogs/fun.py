import discord, typing, random, asyncio
from datetime import datetime
from discord.ext import commands
import re

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

    @commands.command()
    async def squaredraw(self, ctx, *lines: SquareDraw):
        '''
            Draws an image with emoji squares.
            Made by Clari (💜Clari#7744)

            How to use:
                Use a letter below to represent the color of each square, and a number following the letter
                to represent the number of squares of that color. The number of squares is optional.
                Example:
                    `k2r3k2`
                You can also use groups, like this:
                    `(3x(k2r3k2))`

            Colors:
                - k - black
                - w - white
                - r - red
                - o - orange
                - y - yellow
                - g - green
                - p - purple
                - n - brown
                - ; - newline (or space)              
            
            Example:
                `;squaredraw (4x(4xkw);(4xwk);)`
        '''
        return await ctx.send(embed=discord.Embed(title='Here\'s your monster', description='\n'.join(lines)))

    @commands.command()
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

def setup(bot):
    bot.add_cog(Fun(bot))