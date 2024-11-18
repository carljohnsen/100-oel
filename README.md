# 100 øl på 100 minutter
Automated spotify control that fades in and out between 100 songs, every minute, where it plays an interlude sound indicating that it's time to drink.

# Setup
This only work with a spotify premium account, as the Spotify API requires a premium account to control playback.

## Requirements
This project is built using Python 3 and has been tested with Python 3.11.10.

To install the required packages:
```
pip3 install -r requirements.txt
```

## Spotify API
Follow [the spotipy setup instructions](https://spotipy.readthedocs.io/en/latest/#getting-started):
- Create a Spotify app
- Get your client ID and client secret
- Set your client ID and client secret as environment variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Determine which device should play the music
To determine which device should play the music, run the following command:
```
python3 print_devices.py
```
This will print a list of devices that are available to play music. Copy the device ID of the device you want to play music on and export it as an environment variable:
```
export SPOTIPY_DEVICE_ID='your-device-id'
```

# Usage
## Building the tracklist
To build the tracklist, run the following command:
```
python3 [trackname] [artist]
```
This will present you with a list of songs that match the search query. Select the song you want to add to the tracklist by entering the number of the song. This will also play the song on the device you specified. It will then ask you whether you'd like that added to the tracklist. You can put either `y`, `n` or the starting point in the song in seconds. If you put the starting point in seconds, the song will start at that point in the tracklist during the 100 minutes main run.

The tracklist is saved in `tracklist.json` and is a list of dictionaries with the following keys:
- `index`: The index of the song in the tracklist. This is ignored, and is only used for human readability.
- `id`: The Spotify ID of the song.
- `name`: The name of the song.
- `artist`: The artist of the song.
- `position`: The position (in seconds) in the song where the song should start.
- `duration`: The duration of the song in milliseconds.
The tracklist is played in the order it is in the `tracklist.json` file.

## Preparing the interlude sounds
Every minute, an interlude sound will play to indicate that it's time to drink. To prepare the interlude sounds, create a folder named `interlude` and fill it with the possible sounds. Every minute, the script picks one at random. Note that it is blocking until the sound is done playing, so it should be short.

## Running the main script
To run the main script, run the following command:
```
python3 oel.py [index]
```
Which starts going through the tracklist sequentially, starting at `index` (0-indexed). If no index is provided, it will start at the beginning of the tracklist. The index is included in case the script crashes and you want to resume from where you left off.

## Saving the tracklist as a spotify playlist
To save the tracklist as a Spotify playlist, run the following command:
```
python3 save_playlist.py
```
This will save the tracklist as a public Spotify playlist under your usere named `100 Øl`.
