import discord
from discord import embeds
from discord.colour import Colour
from discord.ext.commands.cog import Cog
from services import Anime
from discord.ext import commands
import asyncio



class AnimeInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.anime =  Anime(url="https://api.jikan.moe/v3/")

    def anime_detail(self, mal_id):
        detail = self.anime.get_info_of_anime(mal_id)
        detail_embed = discord.Embed(
            title = detail.get("title"), description ="( "+detail.get('title_japanese')+" )\n"+"Status: "+ detail.get("status"), color=Colour.dark_gold())
        detail_embed.set_image(url=detail.get("image_url"))
        trailer = detail.get("trailer_url")
        detail_embed.add_field(name='Trailer',value=f"[trailer]({trailer})")
        return detail_embed

    @commands.command()
    async def top(self, ctx):
        top_anime = self.anime.get_list_top_anime()
        top_embed = discord.Embed(title = "KaWaii", color = Colour.dark_purple())
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+top_anime[i].get('title'))
            index += 1
        top_embed.add_field(name="Top Airing Anime ", value='\n'.join(list_of_title), inline=True)
        top_embed.add_field(name="See more", value="Type: `k!>>`\n Detail: `number`", inline=False)

        await ctx.send(embed= top_embed)

    @commands.command()
    async def s(self, ctx, name):
        anime = self.anime.get_anime_by_name(name)
        

    @commands.command()
    async def ss(self,ctx, year, season):
        ss_anime = self.anime.get_anime_list_byYearandSs(season,year)
        ss_embed = discord.Embed(title = "KaWaii", color = Colour.dark_orange())
        ss_embed.set_thumbnail(url="https://giffiles.alphacoders.com/132/132620.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+ss_anime[i].get('title'))
            index += 1
        ss_embed.add_field(name=f"{season.upper()} {year} Anime", value='\n'.join(list_of_title), inline=False)
        ss_embed.add_field(name="See more", value="Type: `k!>>`", inline=True)
        ss_embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= ss_embed)

        def check(m):
            global the_message
            if m.author == ctx.author:
                the_message = m.content
                return m.content.isdigit()

        try:
            await self.client.wait_for('message', check = check, timeout=180)
            if the_message.lower().isdigit()==True:
                await ctx.send(embed = self.anime_detail(ss_anime[int(the_message)-1].get("mal_id")))
            else:
                ctx.send('Invalid')
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long")
            

def setup(client):
    client.add_cog(AnimeInfo(client))