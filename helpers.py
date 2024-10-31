import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

device_id = os.environ['SPOTIPY_DEVICE_ID']

def get_spotify_client():
    # Set up the client credentials
    scope = "app-remote-control,streaming,user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

