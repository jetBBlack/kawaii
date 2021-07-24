import discord
from discord.ext import commands
import datetime

class AdminCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @commands.command(aliases = ["member_count", "count"])
    async def members(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Member Count", icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(AdminCommands(client))