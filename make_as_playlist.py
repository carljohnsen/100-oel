import argparse
import helpers
import json

parser = argparse.ArgumentParser(description='Creates a new playlist on spotify using the given tracklist. The playlist will be named "100 Øl"')
parser.add_argument('tracklist', type=str, help='The file containing the tracklist')
args = parser.parse_args()

sp = helpers.get_spotify_client()
uid = sp.me()['id']

with open(args.tracklist, 'r') as f:
    tracklist = json.load(f)["tracks"]

sp.user_playlist_create(uid, '100 Øl', public=True)

for track in tracklist:
    sp.user_playlist_add_tracks(uid, sp.current_user_playlists()['items'][0]['id'], [track['id']])