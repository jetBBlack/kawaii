import discord
import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands

client = commands.Bot(command_prefix=['k!', 'K!'],case_insensitive=True)

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
#         await ctx.send(error)

@client.command()
async def guide(ctx):
    embed = discord.Embed(
        title="Hello! I'm Kawaii", description= "Below is all command you can do with KaWaii", color = discord.Colour.from_rgb(255,99,7))
    embed.set_thumbnail(url="https://images7.alphacoders.com/695/thumb-1920-695212.png")
    embed.add_field(
        name="ANIME INFORMATION", value="""
        `k!top`- Show a list of top anime of all time
        `k!ss [season] [year]`- Show a list of anime of the specified season
        `k!nextss` - Show the list of anime of the next season
        `k!c [character name]` - See infomation of character
        """)
    
    await ctx.send(embed = embed)


load_dotenv()
client.run(os.getenv('TOKEN'))

