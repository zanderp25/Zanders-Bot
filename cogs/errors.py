import discord
from cogs import guild
from discord.ext import commands
from discord.ext.commands.core import command

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:Exception):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{ctx.invoked_with} is missing an argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{ctx.invoked_with} is using an invalid argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"I don't have permission to do this", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                embed=discord.Embed(title=f"This command can't be used in private messages", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.DisabledCommand):
            await ctx.reply(
                embed=discord.Embed(title=f"This command is disabled", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(
                embed=discord.Embed(title=f"Error while executing command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}\n"
                    "**Error:**```py\n{error}\n```"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, guild.NotInGuild):
            await ctx.reply(
                embed=discord.Embed(title=f"You're not in the correct guild.", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {ctx.invoked_with} for more info"
                )
            )

def setup(bot):
    bot.add_cog(Errors(bot))