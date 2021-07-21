import discord
from discord.ext import commands
from discord.ext.commands.core import command

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:Exception):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{ctx.command.name} is missing an argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{ctx.command.name} is using an invalid argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"I don't have permission to do this", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.reply(
                embed=discord.Embed(title=f"This command can't be used in private messages", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.DisabledCommand):
            await ctx.reply(
                embed=discord.Embed(title=f"This command is disabled", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.reply(
                embed=discord.Embed(title=f"Error while executing command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.command.signature}\n**Error:**```py\n{error}\n```"
                ).add_footer(
                    text=f"Type {ctx.prefix}help {ctx.command.name} for more info"
                )
            )

def setup(bot):
    bot.add_cog(Errors(bot))