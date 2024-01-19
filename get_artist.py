#installed requests and python-dotenv

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")          #get ID from .env file
client_secret = os.getenv("CLIENT_SECRET")  #get secret from .env file

def get_auth_header():
    #creates token to access spotify API and uses it to make authorization header.
    auth_string = client_id + ":" + client_secret
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

def search_artist(headers, artist_name):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_name}&type=artist&limit=1"

    full_url = url + query
    result = get(full_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if(len(json_result) == 0):
        print("Could not find artist. Try a different name.")
        return None
    
    return json_result[0]

def get_songs_by_artist(headers, artist_id, country):
    #Take in two digit country code
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

headers = get_auth_header()

artist = "Chappell Roan"

artist_name = search_artist(headers, artist)['name']
artist_id = search_artist(headers, artist)['id']

#print(artist_id)

all_songs = get_songs_by_artist(headers, artist_id, "US")

for idx, song in enumerate(all_songs):
    print(f"{idx +1}", f"{song['name']}")