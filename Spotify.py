#installed requests and python-dotenv

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

#My User Info:
client_id = os.getenv("CLIENT_ID")          #get ID from .env file
client_secret = os.getenv("CLIENT_SECRET")  #get secret from .env file

class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.header = self.get_auth_header()

    def get_auth_header(self):
        #creates token to access spotify API and uses it to make authorization header.
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type":"client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)

        token = json_result["access_token"]
        return {"Authorization": "Bearer " + token}

    def search_artist(self, artist_name):
        headers = self.header
        url = "https://api.spotify.com/v1/search"
        query = f"?q={artist_name}&type=artist&limit=1"

        full_url = url + query
        result = get(full_url, headers = headers)
        json_result = json.loads(result.content)["artists"]["items"]

        if(len(json_result) == 0):
            print("Could not find artist. Try a different name.")
            return None
        
        return json_result[0]

    def print_top_10_songs_by_artist(self, artist_name, country):
        #Take in two digit country code
        headers = self.header
        artist_id = self.search_artist(artist_name)['id']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"

        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        
        for idx, song in enumerate(json_result):
            print(f"{idx +1}", f"{song['name']}")

    def recommend_artists(self, artist):
        headers = self.header
        artist_name = self.search_artist(artist)['name'] #Added this line to get correct spelling for artist
        artist_id = self.search_artist(artist)['id']
        url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"

        result = get(url, headers=headers)
        json_result = json.loads(result.content) #Returns dictionary with 'artists' key and list value
        
        print(f"If you like {artist_name}, you might like the following artists:")
        for idx, elem in enumerate(json_result['artists']):
            print(f"{idx+1}.", f"Name: {elem['name']}","\n\t", f"Popularity: {elem['popularity']}")

#Example Implementation:
user1 = Spotify(client_id, client_secret) #Define user
artist = "Hayley Kiyoko" #Artist name that you're interested in

artist_info = user1.search_artist(artist)
artist_name = user1.search_artist(artist)['name']
all_songs = user1.print_top_10_songs_by_artist(artist_name, "US")

#user1.recommend_artists(artist)
print("\n\n\n")
print(user1.recommend_artists(artist))