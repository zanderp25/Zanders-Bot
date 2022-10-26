import discord
from datetime import datetime
from discord.ext import commands

class RoombaLeg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_guild_channel_delete")
    async def on_guild_channel_delete(self: commands.Context, channel: discord.abc.GuildChannel):
        if channel.guild.id != 760908868737302528: return
        if channel.type == discord.ChannelType.text:
            newchan = await channel.guild.create_text_channel(
                name = channel.name, 
                category = channel.category,
                topic = channel.topic,
                overwrites=channel.overwrites,
                position = channel.position,
                reason = "Auto remake deleted channel",
                )
            await newchan.send("smh this channel was deleted")
        elif channel.type == discord.ChannelType.voice:
            newchan = await channel.guild.create_voice_channel(
                name = channel.name, 
                category = channel.category,
                overwrites = channel.overwrites,
                bitrate = channel.bitrate,
                user_limit = channel.user_limit,
                position = channel.position,
                reason = "Auto remake deleted channel",
                )
        elif channel.type == discord.ChannelType.category:
            newchan = await channel.guild.create_category_channel(
                name = channel.name, 
                overwrites = channel.overwrites,
                position = channel.position,
                reason = "Auto remake deleted category",
                )
            for c in channel.channels:
                await c.edit(parent_id=newchan.id)
        else: newchan = None
        await discord.utils.get(channel.guild.channels,name="welcome",type=discord.ChannelType.text).send(
            embed = discord.Embed(
                color = discord.Color.red(), 
                title = f"Channel Deleted", 
                description = f"Channel: {channel.name} ({channel.id})\n"
                f"Type: {channel.type}\n"
                f"User: {(await channel.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_delete).flatten())[0].user.mention}\n"
                f"New channel: {newchan.name} ({newchan.mention})" \
                    if newchan != None else "Could not identify the channel type, could not create a new one.",
                timestamp = datetime.now()
            )
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(RoombaLeg(bot))