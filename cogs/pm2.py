import re, subprocess, asyncio
import discord
from discord.ext import commands

# Defaults
ssh = ""
sort = True
sort_by = "id"

# Core Functions
def list_pm2():
    if ssh == "":
        command = "pm2 ls"
    else:
        command = f'echo "pm2 ls" | ssh {ssh}'

    output = re.findall(
        r'│ ([0-9 ]{3}) │ (.*) │ (.{11}) │ (.{7}) │ (.{7}) │ (.{8}) │ (.{6}) │ (.{4}) │ (.{9}) │ (.{8}) │ (.{8}) │ (.{4,11}) │ (.{8}) │',
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL).stdout.decode(),
    )

    processes = []
    keys = "id name namespace version mode pid uptime restarts status cpu mem user watching".split()
    for p in output:
        processes += [dict(zip(keys, [p[i].strip() for i in range(13)]))]
    try:
        if sort: processes = sorted(processes, key = lambda item: item[sort_by])
    except:
        pass
    return processes

def start_pm2(id):
    if ssh == "":
        command = f"pm2 start {id}"
    else:
        command = f'echo "pm2 start {id}" | ssh {ssh}'
    p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p.returncode

def stop_pm2(id):
    if ssh == "":
        command = f"pm2 stop {id}"
    else:
        command = f'echo "pm2 stop {id}" | ssh {ssh}'
    p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p.returncode

def restart_pm2(id):
    if ssh == "":
        command = f"pm2 restart {id}"
    else:
        command = f'echo "pm2 restart {id}" | ssh {ssh}'
    p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p.returncode

# Discord Module
class PM2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def number_prompt(self, ctx, prompt):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        m = await ctx.send(prompt)
        while True:
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                return -1
            else:
                if msg.content.isnumeric() and int(msg.content) < 0:
                    return int(msg.content)
            
    
    @commands.group(name="pm2", aliases=[], invoke_without_command=True)
    @commands.is_owner()
    async def pm2(self, ctx):
        """Controls PM2 on the server"""
        reactions = {
            "start":  "\U000025b6",
            "reload": "\U0001f501",
            "stop":   "\U000023f9",
        }
        msg = await self.pm2_list(ctx)
        await asyncio.sleep(0.1)
        for reaction in reactions:
            await msg.add_reaction(reactions[reaction])
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=lambda reaction, user: reaction.message.id == msg.id and user == ctx.author)
            except asyncio.TimeoutError:
                return
            else:
                if reaction.emoji == reactions["start"]:
                    proc = await self.number_prompt(ctx, "What process do you want to start? (id)")
                    if proc == -1:
                        return
                    else:
                        m = await ctx.send(f"Starting process {proc}")
                        if start_pm2(proc) == 0:
                            await m.edit(content=f"Process {proc} started")
                        else:
                            await m.edit(content=f"Error starting process {proc}")
                elif reaction.emoji == reactions["reload"]:
                    proc = await self.number_prompt(ctx, "What process do you want to reload? (id)")
                    if proc == -1:
                        return
                    else:
                        m = await ctx.send(f"Reloading process {proc}")
                        if restart_pm2(proc) == 0:
                            await m.edit(content=f"Process {proc} reloaded")
                        else:
                            await m.edit(content=f"Error reloading process {proc}")
                elif reaction.emoji == reactions["stop"]:
                    proc = await self.number_prompt(ctx, "What process do you want to stop? (id)")
                    if proc == -1:
                        return
                    else:
                        m = await ctx.send(f"Stopping process {proc}")
                        if stop_pm2(proc) == 0:
                            await m.edit(content=f"Process {proc} stopped")
                        else:
                            await m.edit(content=f"Error stopping process {proc}")
    
    @pm2.command(name="list", aliases=["ls"])
    async def pm2_list(self, ctx):
        """Lists all processes in PM2"""
        processes = list_pm2()
        if len(processes) == 0:
            await ctx.send("No processes found")
            return
        list_ = "`ID ` `Name              ` `Status ` `Time` `↺     ` `CPU     ` `MEM     `"
        for p in processes:
            list_ += f"\n`{p['id'].ljust(3)}` `{p['name'].ljust(18)}` `{p['status'].ljust(7)}` `{p['uptime'].ljust(4)}` `{p['restarts'].ljust(6)}` `{p['cpu'].ljust(8)}` `{p['mem'].ljust(8)}`"
        embed = discord.Embed(
            title="PM2 Processes",
            description=list_,
            color=0x00ff00,
        ).set_author(
            name=ctx.me.display_name,
            icon_url=ctx.me.avatar.url,
        ).set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar.url,
        )
        return await ctx.send(embed=embed)


    @pm2.command(name="start", aliases=[])
    async def pm2_start(self, ctx, id):
        """Starts a process"""
        if start_pm2(id) == 0:
            await ctx.send(f"Process {id} started")
        else:
            await ctx.send(f"Process {id} not found")
        
    @pm2.command(name="stop", aliases=[])
    async def pm2_stop(self, ctx, id):
        """Stops a process"""
        if stop_pm2(id) == 0:
            await ctx.send(f"Process {id} stopped")
        else:
            await ctx.send(f"Process {id} not found")

    @pm2.command(name="restart", aliases=[])
    async def pm2_restart(self, ctx, id):
        """Restarts a process"""
        if restart_pm2(id) == 0:
            await ctx.send(f"Process {id} restarted")
        else:
            await ctx.send(f"Process {id} not found")

async def setup(bot):
    await bot.add_cog(PM2(bot))

# CLI
if __name__ == "__main__":
    while True:
        e = input("pm2 > ")
        if e == "exit":
            break
        elif e == "list":
            print("PM2 List:")
            processes = list_pm2()
            if len(processes) == 0:
                print("No processes found")
            else:
                for p in processes:
                    print(f"{p['id']}: {p['name']} - {p['status']} {p['uptime']} ↺: {p['restarts']} CPU: {p['cpu']} Memory: {p['mem']}")
        elif e == "start":
            id = input("ID: ")
            if start_pm2(id) == 0:
                print("Started")
            else:
                print("Error")
        elif e == "stop":
            id = input("ID: ")
            if stop_pm2(id) == 0:
                print("Stopped")
            else:
                print("Error")
        elif e == "restart":
            id = input("ID: ")
            if restart_pm2(id) == 0:
                print("Restarted")
            else:
                print("Error")
        elif e == "settings":
            print("Settings:")
            print(f"ssh: {ssh}")
            print(f"sort: {sort}")
            print(f"sort_by: {sort_by}")
            while True:
                e = input("settings > ")
                if e == "exit":
                    break
                elif e == "ssh":
                    print("Enter the IP and flags to connect via SSH or leave blank for none.")
                    ssh = input("ssh > ")
                elif e == "sort":
                    sort = input("Do you want to sort the list? (y/n) > ")
                    if sort == "y":
                        sort = True
                    elif sort == "n":
                        sort = False
                    else:
                        print("Invalid input.")
                elif e == "sort_by":
                    print("Enter the key to sort by or leave blank for id.")
                    sort_by = input("sort_by > ")
                    if sort_by == "":
                        sort_by = "id"
                elif e == "view":
                    print("Settings:")
                    print(f"ssh: {ssh}")
                    print(f"sort: {sort}")
                    print(f"sort_by: {sort_by}")
                elif e == "help":
                    print("Available commands:")
                    print("ssh")
                    print("sort")
                    print("sort_by")
                    print("view")
                    print("exit")
                elif e == "":
                    pass
                else:
                    print("Invalid command.")
        elif e == "help":
            print("Available commands:")
            print("list")
            print("start")
            print("stop")
            print("restart")
            print("settings")
            print("exit")
        elif e == "":
            pass
        else:
            print("Invalid command.")