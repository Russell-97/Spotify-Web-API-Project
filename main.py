import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

# Define scopes: https://developer.spotify.com/documentation/web-api/concepts/scopes
scope = "user-read-private user-read-email user-library-read playlist-read-private user-top-read"

# Authenticate the user
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Get current user info
user = sp.current_user()

print(" Logged in as:", user["display_name"])
print(" Email:", user["email"])
print(" Country:", user["country"])
print(" User ID:", user["id"])

top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')

print("\nTop 10 Artists:")
for idx, artist in enumerate(top_artists['items'], start=1):
    print(f"{idx}. {artist['name']}")

# Get user's top tracks
top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')

print("\nTop 10 Tracks:")
for idx, track in enumerate(top_tracks['items'], start=1):
    artist_names = ", ".join([artist['name'] for artist in track['artists']])
    print(f"{idx}. {track['name']} by {artist_names}")