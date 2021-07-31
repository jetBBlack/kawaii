import discord
from discord.colour import Colour
from discord.ext.commands.cog import Cog
from services import Anime
from discord.ext import commands
import asyncio
import random
from datetime import date

class AnimeCharacters(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.emoji = [u"\U0001F44D",u"\U0001F496"]
        self.anime =  Anime(url="https://api.jikan.moe/v3/")

    def character_detail(self, mal_id):
        detail = self.anime.get_info_of_character(mal_id)
        embeds = discord.Embed(title =str(detail.get('name'))+" ("+ str(detail.get('name_kanji')) +")",color=Colour.dark_gray())
        embeds.set_author(icon_url="https://cdn.myanimelist.net/images/characters/10/352557.jpg?s=ae2021d50c110379233086db8c4c8ff3", name='Character with KaWaii')
        embeds.set_image(url=detail.get('image_url'))
        embeds.add_field(name='Anime',value=detail.get('animeography')[0].get('name'), inline=False)
        #embeds.add_field(name='About',value=detail.get('about'), inline=False)
        return embeds

    @commands.command()
    async def topc(self, ctx):
        top_char = self.anime.get_list_top_character()
        embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
        embed.set_thumbnail(url="https://giffiles.alphacoders.com/262/26208.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+f"`{top_char[i].get('title')}`"+" - Anime: "+ top_char[i].get('animeography')[0].get('name') )
            index += 1
        embed.add_field(name=f"Top Characters", value='\n'.join(list_of_title), inline=False)
        embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= embed)

        C = True
        def check(m):
            global the_message
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content == "cancel":
                C = False
                raise ValueError("Request cancelled")
        
        while C:
            try:
                await self.client.wait_for('message', check = check, timeout=120)
                if the_message.lower().isdigit()==True:
                    message = await ctx.send(embed = self.character_detail(top_char[int(the_message)-1].get("mal_id")))
                    await message.add_reaction(self.emoji[1])
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
    
    @commands.command()
    async def sc(self, ctx,*, name:str):
        format_name = name.replace(' ', '%')
        char = self.anime.get_list_character_byName(format_name)
        embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
        embed.set_thumbnail(url="https://giffiles.alphacoders.com/262/26208.gif")
        list_of_title = []
        index = 1
        for i in range(len(char)):
            if not len(char[i].get('anime')):
                list_of_title.append(str(index)+". "+char[i].get('name')+" - Anime: ")
            else:
                 list_of_title.append(str(index)+". "+f"`{char[i].get('name')}`"+" - Anime: "+ char[i].get('anime')[0].get('name') )
            
            index += 1
        embed.add_field(name=f"Search result for {name}", value='\n'.join(list_of_title), inline=False)
        embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= embed)

        C = True
        def check(m):
            global the_message
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content.startswith("K!") or m.content == "cancel":
                C = False
                raise ValueError("Request cancelled")
        
        while C:
            try:
                await self.client.wait_for('message', check = check, timeout=120)
                if the_message.lower().isdigit()==True:
                    message = await ctx.send(embed = self.character_detail(char[int(the_message)-1].get("mal_id")))
                    await message.add_reaction(self.emoji[1])
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
    
    @commands.command()
    async def roll(self, ctx):
        card_id = ['118737','155679','118763','118765','45627','17','85', '13','141354','40882','6356','145','136727']
        chosen_id = random.choice(card_id)
        message = await ctx.send(embed = self.character_detail(chosen_id))
        for emoji in self.emoji:
            await message.add_reaction(emoji)

def setup(client):
    client.add_cog(AnimeCharacters(client))
