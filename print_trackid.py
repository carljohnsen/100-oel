import argparse
import helpers
import json
import os

parser = argparse.ArgumentParser(description='Print the current track id')
parser.add_argument('trackname', type=str, help='The name of the track to print the id of')
parser.add_argument('artistname', type=str, help='The name of the artist of the track to print the id of')
args = parser.parse_args()

sp = helpers.get_spotify_client()
did = helpers.device_id

results = sp.search(q=f"track:{args.trackname} artist:{args.artistname}", limit=10, type='track')
items = results['tracks']['items']
n = len(items)

ids = [items[i]['id'] for i in range(n)]
names = [items[i]['name'] for i in range(n)]
artists = [' & '.join([items[i]['artists'][j]['name'] for j in range(len(items[i]['artists']))]) for i in range(n)]
duration = [items[i]['duration_ms'] for i in range(n)]

print ("Top 10 search results:")
for i in range(n):
    print (f'{i}: {ids[i]} "{names[i]}" - "{artists[i]}" ({duration[i] // 1000 // 60}:{duration[i] // 1000 % 60})')

while True:
    index = input('Enter the index of the track to play: ')
    if not index.isdigit() or int(index) < 0 or int(index) >= n:
        print('Invalid index - ignoring')
        exit()
    index = int(index)

    sp.start_playback(device_id=did, uris=[f"spotify:track:{ids[index]}"])

    should_save = input('Do you want to save this track to the tracklist? (y/n/[starting point in s]): ')
    if should_save.isdigit():
        start_pos = int(should_save)
    elif should_save.lower() != 'y':
        start_pos = 0
        continue

    if os.path.exists('tracklist.json'):
        with open('tracklist.json', 'r') as f:
            tracklist = json.load(f)
    else:
        tracklist = {
            "tracks": []
        }

    tracklist["tracks"].append({
        "index": len(tracklist["tracks"]), # For convenience when editing the json
        "id": ids[index], # The Spotify track id
        "name": names[index], # The name of the track
        "artist": artists[index], # The name of the artist
        "position": start_pos, # The position in the track in seconds for when the track should start
        "duration": duration[index] # The duration of the track in milliseconds
    })

    with open('tracklist.json', 'w') as f:
        json.dump(tracklist, f, indent=4)

    break