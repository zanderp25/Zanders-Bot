import discord, subprocess, asyncio
from datetime import datetime
from discord.ext import commands
from jishaku.codeblocks import Codeblock, codeblock_converter


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, x):
        print(x)
        f = open("bot.log", 'a')
        f.write('\n' + x)
        f.close()
    
    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, command):
        time = datetime.now()
        embed = discord.Embed(title=f"Enabled `;{command}``", color=0x06c706)
        ctx.bot.get_command(command).update(enabled=True)
        await ctx.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} enable `;{command}`')

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, command):
        time = datetime.now()
        embed = discord.Embed(title=f"Disabled `;{command}`", color=0xd10606)
        ctx.bot.get_command(command).update(enabled=False)
        await ctx.send(embed=embed)
        await self.log(f'{time} - {ctx.guild} / #{ctx.channel} - {ctx.author} disabled `;{command}`')

    @commands.command()
    @commands.is_owner()
    async def eval(self,ctx, *, argument:codeblock_converter):
        await self.bot.cogs["Jishaku"].jsk_python(ctx=ctx,argument=argument)

    # By Clicks Minute Per
    @commands.command()
    @commands.is_owner()
    async def git(self, ctx):
        m = await ctx.send(embed=discord.Embed(title="Loading..."))
        for r in [834127343206400021, 834148997324472391, 834127343533555713, 834127343525822474, 834127343244673055, 834139266921267211]:  # 834127343576023130
            await m.add_reaction(self.bot.get_emoji(r))
        colours = {
            "delete": 0xF27878,
            "create": 0x68D49E,
            "edit":   0xF2D478,
            "update": 0xF2D478
        }

        gc = {
            "commit": 834127343525822474,
            "pull": 834148997324472391,
            "merge": 834127343533555713,
            "push": 834127343244673055,
            "fetch": 834127343206400021,
            "fork": 834127343576023130,
            "reload": 834139266921267211
        }

        self.head = str(subprocess.check_output(["git", "rev-parse", "HEAD"]))[2:-3]
        self.branch = str(subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]))[2:-3]
        self.commit = str(subprocess.check_output(["git", "show-branch", self.branch]))[(5+(len(self.branch))):-3]
        self.url = str(subprocess.check_output(["git", "config", "--get", "remote.origin.url"]))[2:-3]
        while True:
            await m.edit(embed=(discord.Embed(
                title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                description=f"Current version for `{self.url.split('/')[-2]}/{self.url.split('/')[-1]}`\n"
                            f"**Branch:** `{self.branch}`\n"
                            f"**HEAD:** `{self.head}`\n"
                            f"**Commit:** `{self.commit}`\n\n"
                            f"{self.bot.get_emoji(gc['fetch'])} **Fetch** latest commit\n"
                            f"{self.bot.get_emoji(gc['pull'])} **Pull** fetched version\n"
                            f"{self.bot.get_emoji(gc['merge'])} **Merge** with current version\n"
                            f"{self.bot.get_emoji(gc['commit'])} **Commit** current code\n"
                            f"{self.bot.get_emoji(gc['push'])} **Push** current commit\n\n"
                            f"{self.bot.get_emoji(gc['reload'])} **PM2 reload**",
                color=colours["create"]
            )).set_footer(text="By Clicks Minute Per"))
            try:
                reaction = await ctx.bot.wait_for("reaction_add", timeout=60, check=lambda _, user: user == ctx.author)
            except asyncio.TimeoutError:
                break

            try:
                await m.remove_reaction(reaction[0].emoji, ctx.author)
            except Exception as e:
                print(e)

            if reaction is None:
                break
            elif reaction[0].emoji.name == "Fetch":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['fetch'])} Fetch\n\n>>> Fetching",
                    color=colours["create"]
                ))
                out = subprocess.run(["git", "fetch"], stdout=subprocess.PIPE)
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['fetch'])} Fetch\n\n>>> {'Fetched successfully' if out.returncode == 0 else 'Exited with code `' + out.returncode +'`'}",
                    color=colours["create"]
                ))
                await asyncio.sleep(3)
            elif reaction[0].emoji.name == "Pull":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['pull'])} Pull\n\n>>> Pulling",
                    color=colours["create"]
                ))
                out = subprocess.run(["git", "pull"], stdout=subprocess.PIPE)
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['pull'])} Pull\n\n>>> {'Pulled successfully' if out.returncode == 0 else 'Exited with code `' + out.returncode +'`'}",
                    color=colours["create"]
                ))
                await asyncio.sleep(3)
            elif reaction[0].emoji.name == "Merge":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['merge'])} Merge\n\n>>> Merging",
                    color=colours["create"]
                ))
                out = subprocess.run(["git", "merge"], stdout=subprocess.PIPE)
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['merge'])} Merge\n\n>>> {'Merged successfully' if out.returncode == 0 else 'Exited with code `' + out.returncode +'`'}",
                    color=colours["create"]
                ))
                await asyncio.sleep(3)
            elif reaction[0].emoji.name == "Commit":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['commit'])} Commit\n\n>>> Enter a commit message",
                    color=colours["create"]
                ))
                try:
                    message = await ctx.bot.wait_for("message", timeout=60, check=lambda message: message.author.id == ctx.author.id)
                except asyncio.TimeoutError:
                    break

                try:
                    await message.delete()
                except Exception as e:
                    print(e)
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['commit'])} Commit\n\n>>> Committing",
                    color=colours["create"]
                ))
                out = subprocess.run(["git", "commit", "-am", f'"{message.content}"'], stdout=subprocess.PIPE)
                backn = "\n"
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['commit'])} Commit\n\n>>> {f'Committed successfully with message:{backn} {message.content}' if out.returncode == 0 else 'Exited with code `' + out.returncode +'`'}",
                    color=colours["create"]
                ))
                await asyncio.sleep(3)
            elif reaction[0].emoji.name == "Push":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['push'])} Push\n\n>>> Pushing",
                    color=colours["create"]
                ))
                out = subprocess.run(["git", "push"], stdout=subprocess.PIPE)
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['push'])} Push\n\n>>> {'Pushed successfully' if out.returncode == 0 else 'Exited with code `' + out.returncode +'`'}",
                    color=colours["create"]
                ))
                await asyncio.sleep(3)
            elif reaction[0].emoji.name == "reload":
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['reload'])} PM2 Reload\n\n>>> Reloading",
                    color=colours["create"]
                ))
                try:
                    out = subprocess.run(["pm2", "reload", "3"], stdout=subprocess.PIPE).returncode
                except FileNotFoundError:
                    out = 1
                await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(gc['fork'])} Git Controls",
                    description=f"{self.bot.get_emoji(gc['reload'])} PM2 Reload\n\n>>> {'Reloaded successfully' if out == -2 else 'Exited with code `' + str(out) +'`'}",
                    color=colours["create"]
                ))
                return

def setup(bot):
    bot.add_cog(Dev(bot))