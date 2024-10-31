import argparse
import helpers

parser = argparse.ArgumentParser(description='Print the current track id')
parser.add_argument('trackid', type=str, help='The id to play')
args = parser.parse_args()

sp = helpers.get_spotify_client()
did = helpers.device_id

sp.start_playback(device_id=did, uris=[f"spotify:track:{args.trackid}"])