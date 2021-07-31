import requests
import json as js
from datetime import date

class Anime:
    def __init__(self, url) -> None:
        self.url = url
    
    def get_list_top_airing_anime(self):
        response = requests.get(self.url+"top/anime/1/airing")
        if response.status_code == 200:
            result ={}
            result = js.loads(response.text)
            return result.get("top")
        else:
            print("Failed to get data")

    def get_list_top_anime_alltime(self):
        response = requests.get(self.url+"top/anime/1")
        if response.status_code == 200:
            result ={}
            result = js.loads(response.text)
            return result.get("top")
        else:
            print("Failed to get data")
    
    def get_list_upcomming_featured(self):
        response = requests.get(self.url+"season/later")
        if response.status_code == 200:
            result ={}
            result = js.loads(response.text)
            return result.get("anime")
        else:
            print("Failed to get data")

    def get_curr_ss_anime_list(self):
        today = date.today()
        cur_season = ''
        spring = [2,3,4]
        summer = [5,6,7]
        fall = [8,9,10]
        winter = [11,12,1]
        if today.month in spring:
            cur_season = 'spring'
        elif today.month in summer:
            cur_season = "summer"
        elif today.month in fall:
            cur_season = "fall"
        elif today.month in winter:
            cur_season = "winter"
        response = requests.get(self.url+f"season/{today.year}/{cur_season}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get("anime")   
        else:
            print('Failed to get data')
    
    def get_next_ss_anime_list(self):
        today = date.today()
        next_season = ''
        next_year = 0
        spring = [2,3,4]
        summer = [5,6,7]
        fall = [8,9,10]
        winter = [11,12,1]
        if (today.month+3) in spring:
            next_season = 'spring'
        elif (today.month+3) in summer:
            next_season = "summer"
        elif (today.month+3) in fall:
            next_season = "fall"
        elif (today.month+3) in winter:
            next_season = "winter"

        if today.month in [11, 12]:
            next_year = today.year+1
        else: next_year = today.year
        
        response = requests.get(self.url+f"season/{next_year}/{next_season}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get("anime")   
        else:
            print('Failed to get data')

    def get_anime_list_byYearandSs(self, season, year):
        response = requests.get(f"{self.url}season/{year}/{season}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get("anime")
        else: 
            print('Failed to get data')
    
    def search_by_name(self, name, type):
        response = requests.get(f"{self.url}search/{type}?q={name}&limit=10")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.content)
            return result.get("results")
        else: 
            print('Failed to get data')

    def get_info_of_anime(self, anime_id, type='anime'):
        response = requests.get(f"{self.url}{type}/{anime_id}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.content)
            return result
        else:
            print('Failed to get data from API')

    def get_top_manga(self, type):
        response = requests.get(f"{self.url}top/manga/1/{type}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get('result')
        else:
            print('Invalid type')

    def get_list_character_byName(self, name):
        response = requests.get(f"{self.url}search/character?q={name}&limit=10")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get('results')
        else: 
            print('Failed to get data')
    
    def get_list_top_character(self):
        response = requests.get(f"{self.url}/top/characters/1/")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.content)
            return result.get('top')
        else:
            print('Failed to get data')
    
    
#Test request
# anime = Anime("https://api.jikan.moe/v3/")
# new_ss_list = anime.get_list_character_byName("Chtholly")
# for i in range(len(new_ss_list)):
#     print(new_ss_list[i].get('name'))



