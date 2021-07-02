import requests
import json as js

class Anime:
    def __init__(self, url) -> None:
        self.url = url
        
    def get_next_ss_anime_list(self):
        response = requests.get(self.url+"season/later")
        list_of_title = []
        if (response.status_code == 200):
            result = {}
            result = js.loads(response.text)
            index = 1
            item = result.get("anime")
            for i in range(10):
                list_of_title.append(str(index)+". "+item[i].get('title'))
                index +=1
            return list_of_title 
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

    def get_info_of_anime(self, anime_id, request):
        response = requests.get(f"{self.url}anime/{anime_id}/{requests}")
        if (response.status_code == 200):
            result = {}
            result = js.load(response.content)
            if (request == 'characters_staff'):
                return result.get("characters")
            elif (request == 'episodes'):
                return result.get("episodes")
            elif (request == 'news'):
                return result.get("news")
            elif (request == 'videos'):
                return result.get("promo")
        else:
            print('Failed to get data')
                 

# anime = Anime("https://api.jikan.moe/v3/")
# new_ss_list = anime.fecth_next_ss_anime_list()
# for i in new_ss_list:
#     print(i)