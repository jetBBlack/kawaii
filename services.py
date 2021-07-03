import requests
import json as js

from requests.models import Response

class Anime:
    def __init__(self, url) -> None:
        self.url = url
    
    def get_list_top_anime(self):
        response = requests.get(self.url+"top/anime/1/airing")
        if response.status_code == 200:
            result ={}
            result = js.loads(response.content)
            return result.get("top")
        else:
            print("Failed to get data")

    def get_next_ss_anime_list(self):
        response = requests.get(self.url+"season/later")
        list_of_title = []
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
    
    def get_anime_by_name(self, name):
        response = requests.get(f"{self.url}search/anime?q={name}&limit=10")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            return result.get("results")
        else: 
            print('Failed to get data')
    
    def get_mange_by_name(self, name):
        response = requests.get(f"{self.url}search/manga?q={name}&limit=10")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.content)
            return result.get("results")
        else: 
            print('Failed to get data')

    def get_info_of_anime(self, anime_id):
        response = requests.get(f"{self.url}anime/{anime_id}")
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.content)
            return result
        else:
            print('Failed to get data')
                 

# anime = Anime("https://api.jikan.moe/v3/")
# new_ss_list = anime.get_info_of_anime(41487)
# print(new_ss_list)
