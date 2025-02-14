import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    # Set up the client credentials
    scope = "app-remote-control,streaming,user-read-playback-state,user-modify-playback-state,user-read-currently-playing, playlist-modify-public"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def parse_environment():
    global device_id

    env_dict = dict()
    if os.path.exists('secrets.env'):
        with open('secrets.env') as f:
            for line in f:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    env_dict[parts[0]] = parts[1]

    keys_to_set = ['SPOTIPY_CLIENT_ID', 'SPOTIPY_CLIENT_SECRET', 'SPOTIPY_REDIRECT_URI']
    for key in keys_to_set:
        if key not in os.environ:
            if key in env_dict:
                os.environ[key] = env_dict[key]
            else:
                raise Exception(f"Environment variable {key} not set in either secrets file nor environment.")

    # Device ID is a special case, as it's not initially set.
    if 'SPOTIPY_DEVICE_ID' in os.environ:
        device_id = os.environ['SPOTIPY_DEVICE_ID']

parse_environment()