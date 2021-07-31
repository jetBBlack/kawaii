import discord
from discord import embeds
from discord.colour import Colour
from discord.ext.commands.cog import Cog
from services import Anime
from discord.ext import commands
import asyncio
from datetime import date


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
        elif not len(op) and len(ed):
            detail_embed.add_field(name='OST', value='**OP themes**:  \n **ED themes**: {}'.format(ed[0]), inline=False)
        elif not len(ed) and len(op):
            detail_embed.add_field(name='OST', value='**OP themes**: {}  \n **ED themes**: '.format(op[0]), inline=False)
        else:
            detail_embed.add_field(name='OST', value='**OP themes**: {} \n **ED themes**: {}'.format(op[0],ed[0]), inline=False)

        detail_embed.set_footer(text=detail.get('studios')[0].get("name")+" studio")
        return detail_embed

    @commands.command()
    async def top(self, ctx):
        top_anime = self.anime.get_list_top_anime_alltime()
        top_embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
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
                await self.client.wait_for('message', check = check, timeout=150)
                if the_message.lower().isdigit()==True:
                    await ctx.send(embed = self.anime_detail(top_anime[int(the_message)-1].get("mal_id")))
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
               

    @commands.command()
    async def s(self, ctx, *,name:str):
        n_name = name.replace(' ', '%')
        anime = self.anime.get_anime_by_name(n_name)
        embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
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
            await self.client.wait_for('message', check = check, timeout=150)
            if the_message.lower().isdigit()==True:
                await ctx.send(embed = self.anime_detail(anime[int(the_message)-1].get("mal_id")))  
        except asyncio.TimeoutError:
            await ctx.send("`Session timeout`")
        
    @commands.command()
    async def ss(self,ctx, year, season):
        ss_anime = self.anime.get_anime_list_byYearandSs(season,year)
        ss_embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
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
                    await ctx.send(embed = self.anime_detail(ss_anime[int(the_message)-1].get("mal_id")))
                elif the_message.isdigit()==False:
                    ctx.send('Invalid number')
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Sorry, session timeout")
    
    @commands.command()
    async def currentss(self, ctx):
        curr_ss = self.anime.get_curr_ss_anime_list()
        ss_embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
        ss_embed.set_thumbnail(url="https://giffiles.alphacoders.com/132/132620.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+curr_ss[i].get('title'))
            index += 1
        ss_embed.add_field(name=f"Current Season Anime List", value='\n'.join(list_of_title), inline=False)
        ss_embed.add_field(name="See more", value="Type: `k!>>`", inline=True)
        ss_embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= ss_embed)

        C = False
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
                    await ctx.send(embed = self.anime_detail(curr_ss[int(the_message)-1].get("mal_id")))
                elif the_message.isdigit()==False:
                    ctx.send('Invalid number')
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")

    @commands.command()
    async def nextss(self, ctx):
        next_ss = self.anime.get_next_ss_anime_list()
        ss_embed = discord.Embed(title = "KaWaii", color = Colour.dark_orange())
        ss_embed.set_thumbnail(url="https://giffiles.alphacoders.com/132/132620.gif")
        list_of_title = []
        index = 1
        for i in range(12):
            list_of_title.append(str(index)+". "+next_ss[i].get('title'))
            index += 1
        ss_embed.add_field(name=f"Next Season Anime List", value='\n'.join(list_of_title), inline=False)
        ss_embed.add_field(name="See more", value="Type: `k!>>`", inline=True)
        ss_embed.add_field(name="See detail", value="Select `[number]` to see detail", inline=True)
        await ctx.send(embed= ss_embed)

        C = False
        def check(m):
            global the_message
            if m.author == ctx.author and m.content.startswith("k!")==False and m.content !="cancel":
                the_message = m.content
                return m.content.isdigit() == True
            elif m.content.startswith("k!") or m.content.startswith("K!") or m.content == "cancel":
                C = False
                raise ValueError("Session timeout")

        while C:
            try:
                await self.client.wait_for('message', check = check, timeout=120)
                if the_message.lower().isdigit()==True:
                    await ctx.send(embed = self.anime_detail(next_ss[int(the_message)-1].get("mal_id")))
                elif the_message.isdigit()==False:
                    ctx.send('Invalid number')
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
    
    @commands.command()
    async def upcoming(self, ctx):
        upcoming = self.anime.get_list_upcomming_featured()
        embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
        embed.set_thumbnail(url="https://giffiles.alphacoders.com/262/26208.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+upcoming[i].get('title'))
            index += 1
        embed.add_field(name=f"Top Upcoming", value='\n'.join(list_of_title), inline=False)
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
                    await ctx.send(embed = self.anime_detail(upcoming[int(the_message)-1].get("mal_id")))
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
    
    @commands.command()
    async def topairing(self, ctx):
        airing = self.anime.get_list_top_airing_anime()
        embed = discord.Embed(title = "KaWaii", color = Colour.from_rgb(255,99,71))
        embed.set_thumbnail(url="https://giffiles.alphacoders.com/262/26208.gif")
        list_of_title = []
        index = 1
        for i in range(10):
            list_of_title.append(str(index)+". "+airing[i].get('title'))
            index += 1
        embed.add_field(name=f"Top Upcoming", value='\n'.join(list_of_title), inline=False)
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
                    await ctx.send(embed = self.anime_detail(airing[int(the_message)-1].get("mal_id")))
            except asyncio.TimeoutError:
                C = False
                await ctx.send("Session timeout")
    
   
def setup(client):
    client.add_cog(AnimeInfo(client))