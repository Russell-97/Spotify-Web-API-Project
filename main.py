from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set up Spotify client with client credentials manager
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Ask user for artist name
artist_name = input("Enter artist name to get their popular tracks and genres: ")

# Search for the artist
results = sp.search(q=artist_name, type="artist", limit=1)

# Check if any artist was found
if not results["artists"]["items"]:
    print("Artist not found.")
    exit()

# Extract artist info
artist = results["artists"]["items"][0]
artist_id = artist["id"]
artist_name = artist["name"]
artist_genres = artist["genres"]

print(f"\nTop Tracks for {artist_name}:\n")

# Get artist's top tracks
top_tracks = sp.artist_top_tracks(artist_id, country="US")

# Print the track names
for idx, track in enumerate(top_tracks["tracks"], start=1):
    print(f"{idx}. {track['name']}")

if artist_genres:
    print("Genres:")
    for genre in artist_genres:
        print(f" - {genre}")
else:
    print("No genres available for this artist.")
