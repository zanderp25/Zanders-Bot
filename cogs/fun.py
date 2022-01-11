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
        return await ctx.send(embed=discord.Embed(title='Here\'s your monster', description='\n'.join(lines)))

    @commands.command()
    async def bubbles(self, ctx, width:int, height:int):
        width = width if 0<width<=10 else 10
        height = height if 0<height <=20 else 20
        await ctx.send((('pop'*width)+'\n')*height)

def setup(bot):
    bot.add_cog(Fun(bot))