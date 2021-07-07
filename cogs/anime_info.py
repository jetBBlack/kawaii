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
            title = detail.get("title")+" (_Score_: "+str(detail.get("score"))+")", description =detail.get('title_japanese')+"\n"+"Status: "+ detail.get("status"), color=Colour.dark_gold())
        detail_embed.set_image(url=detail.get("image_url"))
        trailer_url = detail.get("trailer_url")
        type_of_anime = detail.get("type")
        premiered = detail.get('aired').get('string')
        epsodes = detail.get('episodes')
        season = detail.get('premiered')
        op = detail.get('opening_themes')
        ed = detail.get('ending_themes')
        detail_embed.add_field(name='Information'
            ,value=f"[Trailer]({trailer_url}), Type: {type_of_anime}, Season: {season}, Episodes: {epsodes}\n Primiere date: {premiered}", inline=False)
       
        if not len(op) and not len(ed):
             detail_embed.add_field(name='OST', value='**OP themes**:  \n **ED themes**: ', inline=False)
        else:
            detail_embed.add_field(name='OST', value='**OP themes**: {} \n **ED themes**: {}'.format(op[0],ed[0]), inline=False)

        detail_embed.set_footer(text=detail.get('studios')[0].get("name")+" studio")
        return detail_embed

    @commands.command()
    async def top(self, ctx):
        top_anime = self.anime.get_list_top_anime_alltime()
        top_embed = discord.Embed(title = "KaWaii", color = Colour.dark_orange())
        top_embed.set_thumbnail(url="https://giffiles.alphacoders.com/132/132620.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+top_anime[i].get('title'))
            index += 1
        top_embed.add_field(name="Top Anime ", value='\n'.join(list_of_title), inline=False)
        top_embed.add_field(name="See more", value="Type: `k!>>`", inline=True)
        top_embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= top_embed)

        def check(m):
            global the_message
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content == "cancel":
                raise ValueError("Request cancelled")

        try:
            await self.client.wait_for('message', check = check, timeout=120)
            if the_message.lower().isdigit()==True:
                await ctx.send(embed = self.anime_detail(top_anime[int(the_message)-1].get("mal_id")))
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long")

    @commands.command()
    async def s(self, ctx, name):
        anime = self.anime.get_anime_by_name(name)
        embed = discord.Embed(title = "KaWaii", color = Colour.dark_orange())
        embed.set_thumbnail(url="https://giffiles.alphacoders.com/262/26208.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+anime[i].get('title'))
            index += 1
        embed.add_field(name=f"Search result for {name}", value='\n'.join(list_of_title), inline=False)
        embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= embed)

        def check(m):
            global the_message
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content == "cancel":
                raise ValueError("Request cancelled")

        try:
            await self.client.wait_for('message', check = check, timeout=120)
            if the_message.lower().isdigit()==True:
                await ctx.send(embed = self.anime_detail(anime[int(the_message)-1].get("mal_id")))
            
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long")
        

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
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content == "cancel":
                raise ValueError("Request cancelled")

        try:
            await self.client.wait_for('message', check = check, timeout=120)
            if the_message.lower().isdigit()==True:
                await ctx.send(embed = self.anime_detail(ss_anime[int(the_message)-1].get("mal_id")))
            elif the_message.isdigit()==False:
                ctx.send('Invalid number')
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long")
       


def setup(client):
    client.add_cog(AnimeInfo(client))