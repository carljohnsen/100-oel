import argparse
import helpers
import json
import os
import playsound
import random
import time

parser = argparse.ArgumentParser(description='Play the tracks in the tracklist, changing every minute with an interlude.')
parser.add_argument('track_idx_start', type=int, help='The index of the first track to play', nargs='?',action='store', default=0)
parser.add_argument('track_idx_end', type=int, help='The index of the last track to play', nargs='?', action='store', default=100)
args = parser.parse_args()

track_idx_start = args.track_idx_start
track_idx_end = args.track_idx_end

sp = helpers.get_spotify_client()
did = helpers.device_id

# Get the interlude files
interlude_files = [fname for fname in os.listdir('interlude') if fname.endswith('.m4a')]

fade_min = 30
fade_max = 100
fade_seconds = 5
fade_steps = 20
fade_sleep = fade_seconds / fade_steps
fade_stepsize = (fade_max - fade_min) / fade_steps
track_time = 60 - 2*fade_seconds

isp = sp.currently_playing()
if isp is not None and isp['is_playing']:
    sp.pause_playback(device_id=did)

with open('tracklist.json', 'r') as f:
    tracklist = json.load(f)["tracks"]

sp.volume(0, device_id=did)
for i in range(track_idx_start, track_idx_end):
    track = tracklist[i]
    print (f'{i:03d}: {track["id"]} "{track["name"]}" - "{track["artist"]}")')
    sp.start_playback(device_id=did, uris=[f"spotify:track:{track['id']}"], position_ms=int(track['position'])*1000)
    for i in range(fade_steps): # Fade in
        sp.volume(int(fade_min + i*fade_stepsize), device_id=did)
        time.sleep(fade_sleep)
    sp.volume(fade_max, device_id=did)
    time.sleep(track_time)
    for i in range(fade_steps): # Fade out
        sp.volume(int(fade_max - (i*fade_stepsize)), device_id=did)
        time.sleep(fade_sleep)
    sp.volume(fade_min, device_id=did)
    if len(interlude_files) > 0:
        # Choose a random interlude
        interlude = interlude_files[random.randint(0, len(interlude_files) - 1)]
        playsound.playsound(f'interlude/{interlude}')


# Reset the
sp.pause_playback(device_id=did)
sp.volume(100, device_id=did)