import os
from flask import Flask, redirect, request, session, render_template, url_for
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Spotify configuration
SPOTIPY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-read-private user-read-email user-top-read"

# OAuth setup
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    token_info = session.get("token_info")
    if not token_info:
        return redirect('/')

    time_range = request.args.get("time_range", "short_term")  # default to short_term

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)
    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)

    return render_template(
        'index.html',
        user=user,
        artists=top_artists['items'],
        tracks=top_tracks['items'],
        time_range=time_range
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
