import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix=['k!', 'K!'],case_insensitive=True, help_command=None)

@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
    print('Bot ready')

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CommandNotFound):
#         await ctx.send("The command you specified was not found. Type k!help to see all available commands.")
    
#     elif isinstance(error, commands.errors.MissingRequiredArgument):
#          await ctx.send("Sorry. You don't have the permission for that command.")

#     elif isinstance(error, commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
#         await ctx.send("Sorry. You don't have the permission for that command.")

#     else: 
#         await ctx.send(f"`{str(error).split(':')[-1]} `")

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Hello! I'm Kawaii", description= "Below is all command you can do with KaWaii", color = discord.Colour.from_rgb(255,99,7))
    embed.set_thumbnail(url="https://cdn.myanimelist.net/images/characters/10/352557.jpg?s=ae2021d50c110379233086db8c4c8ff3")
    embed.add_field(
        name="ANIME INFORMATION", value="""
        `k!top` - Show a list of top anime of all time
        `k!topairing` - Show a list of top airing anime
        `k!nextss` - Show the list of anime of the next season
        `k!currentss` - Show the list of anime of current season
        `k!ss [season] [year]` - Show a list of anime of the specified season
        `k!s [name]` - Search anime by name
        `k!sc [character name]` - See infomation of character
        `k!topc` - Show a list of top anime character of all time
        `k!roll` - Random character card. And channel members can add reactions to this randomly generated card

        `season`: [spring, summer, fall, winter], `year_format`: yyyy, `name`:utf-8
        `[]` = optional and required information
        """, inline=False)
    embed.add_field(
        name="GUILD", value="""
        `kick`, `ban`, `member`
        """)
    
    await ctx.send(embed = embed)


load_dotenv()
client.run(os.getenv('TOKEN'))

