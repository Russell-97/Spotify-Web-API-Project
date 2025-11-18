import os
from flask import Flask, redirect, request, session, render_template, url_for
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

# Load .env variables
load_dotenv()

# Spotify configuration
SPOTIPY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("REDIRECT_URI")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
SCOPE = "user-read-private user-read-email user-top-read"

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# OAuth setup
def create_spotify_oauth():
    cache_handler = FlaskSessionCacheHandler(session)
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=True   
    )


@app.route('/')
def home():
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        return render_template("login.html")  
    return redirect('/profile')


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    code = request.args.get("code")

    if code:
        sp_oauth.get_access_token(code)

    return redirect('/profile')


@app.route('/profile')
def profile():
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=sp_oauth)

    time_range = request.args.get("range", "short_term") #  default to short_term

    user = sp.current_user()
    top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)['items']
    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)['items']
    top_tracks_album = sp.current_user_top_tracks(limit=50, time_range=time_range)['items']
    top_artists_genre = sp.current_user_top_artists(limit=50, time_range=time_range)['items']
    


    genre_counts = {}
    for artist in top_artists_genre:
        for genre in artist.get("genres", []):
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    top_genres = sorted_genres[:10]

    album_map = {}
    for track in top_tracks_album:
        album = track["album"]
        album_id = album["id"]
        if album_id not in album_map:
            album_map[album_id] = {
                "name": album["name"],
                "image": album["images"][0]["url"] if album["images"] else None
            }

    top_albums = list(album_map.values())[:10]

    return render_template(
        "index.html",
        user=user,
        artists=top_artists,
        tracks=top_tracks,
        genres=top_genres,
        albums=top_albums,
        time_range=time_range
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect("https://accounts.spotify.com/en/logout?continue=" + url_for('home', _external=True))


if __name__ == '__main__':
    app.run(debug=True)
