from Spotify import Spotify

#Needed bc I store my client id and secret in .env file. I use these
#to retrieve that information
from dotenv import load_dotenv
import os

load_dotenv()

#My User Info:
client_id = os.getenv("CLIENT_ID")          #get ID from .env file
client_secret = os.getenv("CLIENT_SECRET")  #get secret from .env file

#Create User Instance for my Account
user1 = Spotify(client_id, client_secret)
header_u1 = user1.get_auth_header()

#What artist do you want to look up?
artist = "Taylor Swift"
artist_info = user1.search_artist(header_u1, artist)
artist_name = user1.search_artist(header_u1, artist)['name']

#Will print top 10 songs for artist you are interested in.
user1.print_top_10_songs_by_artist(header_u1, artist_name, "US")

