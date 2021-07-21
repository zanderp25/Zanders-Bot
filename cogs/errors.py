import discord, random
from cogs import guild
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def e(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:Exception):
        '''The command handler'''

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction('🚫')
            return

        parent_name = ' '.join(ctx.invoked_parents)
        if parent_name != '': parent_name += ' '

        if not type(error) in [
            commands.CommandNotFound,
            commands.CommandOnCooldown,
        ]:
            try:
                await ctx.message.add_reaction('🚫')
                await ctx.bot.get_channel(867254023617642497).send(
                    embed=discord.Embed(
                        color=discord.Color.red(), 
                        title=f"Error running {''.join(ctx.invoked_parents)} {ctx.invoked_with}:", 
                        description=f"```{error}```\n"
                        f"Author: {ctx.author} ({ctx.author.id})\n"
                        f"Channel: {ctx.channel} ({ctx.channel.id})\n"
                        f"Guild: {ctx.guild} ({ctx.guild.id})\n"
                        f"Full message: ```{ctx.message.content}```\n", 
                        timestamp=ctx.message.created_at
                    ).set_author(
                        name=ctx.author.name, 
                        icon_url=ctx.author.avatar_url
                    )
                )
            except:
            pass

        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{parent_name}{ctx.invoked_with} is missing an argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                embed=discord.Embed(title=f"{parent_name}{ctx.invoked_with} is using an invalid argument", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(
                embed=discord.Embed(title=f"I don't have permission to do this", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, guild.NotInGuild):
            await ctx.reply(
                embed=discord.Embed(title=f"You're not in the correct guild.", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                embed=discord.Embed(title=f"This command can't be used in private messages", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                embed=discord.Embed(title=f"This command is on cooldown", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(
                embed=discord.Embed(title=f"You don't have permission to use this command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.DisabledCommand):
            await ctx.reply(
                embed=discord.Embed(title=f"This command is disabled", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(
                embed=discord.Embed(title=f"Error while executing command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}\n"
                    "**Error:**```py\n{error}\n```"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )
        else:
            await ctx.reply(
                embed=discord.Embed(title=f"Error while executing command", 
                color=0xff0000,
                description=f"**Usage:**\n{ctx.prefix}{parent_name}{ctx.invoked_with} {ctx.command.signature}\n"
                    "**Error:**```py\n{error}\n```"
                ).set_footer(
                    text=f"Type {ctx.prefix}help {parent_name}{ctx.invoked_with} for more info"
                )
            )

def setup(bot):
    bot.add_cog(Errors(bot))