import os 
import sys
import json
import csv
import spotipy
import webbrowser
import re
import spotipy.util as util
from typing import List, Dict
from json.decoder import JSONDecodeError

# Get username from terminal
username = sys.argv[1]

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Create Spotify object
spotifyObject = spotipy.Spotify(auth=token)
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))
user = spotifyObject.current_user()

def get_pl_length(pl_uri: str) -> int:
    return spotifyObject.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"

    )["total"]

def get_songlist(pl_uri:str) -> List:
    songlist = []

    offset = 0
    count = 0
    total = 0
    while offset != pl_length:
        # Get next batch of tracks
        

        tracks = spotifyObject.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track.name,total"
        )
        i = 0
        limit = 100
        lower_limit = int(tracks['total'])
        while lower_limit > 100:
            lower_limit -= 100 
        exit_limit = tracks['total'] - lower_limit
        #print(lower_limit)
        if count*100 == exit_limit:
            limit = lower_limit
        
        while i != limit:
            songlist.append(tracks['items'][i]['track']['name'])
            i+=1
        
        #print(count,tracks['items'])
        offset += len(tracks['items'])
        count +=1
        
    return songlist
    
def get_artists(pl_uri:str) -> List[List[Dict]]:
    artists_info = list()
    # Playlist tracks
    offset = 0

    # Only 100 songs at a time problem, loop to keep retrieving 

    while offset != pl_length:
        # Get next batch of tracks
        tracks = spotifyObject.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track.artists.name"
        )

        # Get the list with info of each track from new batch and append 

        [artists_info.append(item["track"]["artists"])
            for item in tracks["items"]
            
            ]
        
        # Update offset
        offset += len(tracks["items"])
    return artists_info

def create_data_csv(name:str, num:str):
    a = open('total.csv', 'w', newline='')
    writer1 = csv.writer(a)
    writer1.writerow([name])

def create_csv(dest:str, artists:List, track_info:List):
    track_file = dest + '_tracks.csv'
    artist_file = 'ft_' + dest + '.csv' 
    g = open(track_file, 'w', newline='')
    h = open(artist_file, 'w', newline='')
    count = 0
    v = 'Track'
    u = 'Artists'
    writer = csv.writer(g)
    writer0 =  csv.writer(h)
    writer.writerow([v])
    writer0.writerow([u])
    while count < len(track_info):
    
        v = track_info[count]    
        writer.writerow([v])
        writer0.writerow(artists[count])

        
        print(count, track_info[count])
        count+=1

pl_id = 'spotify:playlist:5otnNgFTnMpWOFjPChrqu6'
pl_ids = [
    'spotify:playlist:5otnNgFTnMpWOFjPChrqu6', 
    'spotify:playlist:7b46c5syjtG86a77R7SnMs', 
    'spotify:playlist:1zXwFGPTBcGbtV8VNYppvs', 
    'spotify:playlist:3tSzoY3XPBJxWy3FFD05Bx', 
    'spotify:playlist:1it0GYp58l9RLabZUdmvOH',
    'spotify:playlist:69lHZIoSfaMIikQBz5KMFH',
    'spotify:playlist:5wiWly0tLIIKetHVTvhf3P'

]
artist_list = ['eminem', 'drake', 'lil_wayne', 'kanye_west', 'chris_brown', 'kendrick_lamar','nicki_minaj']
num = 0
while num < len(artist_list):
    pl_length = get_pl_length(pl_ids[num])
    print(pl_length)
    
    artists_info = get_artists(pl_ids[num]) # Gets featuring artist info

    track_info = get_songlist(pl_ids[num]) # HAS THE LIST OF SONGS IN THE PLAYLIST THANK GOD
    create_csv(artist_list[num], artists_info, track_info)
    num+=1
create_data_csv(artist_list[num], pl_length)


# Song name, Artist, Featuring Artists, Streams, Year

# Retrieve 12 artist song list 
# Young Thug, Drake, Eminem, Travis Scott, Future, Juice WRLD, 
# Kendrick Lamar, Lil Pump, J. Cole, Akon, Lil Wayne, Lil Tecca

#print(track_info)
#print(json.dumps(artists_info, sort_keys=True, indent=4))
#for item in artists_info:
#    if len(item) > 1:
#        i = 0
#        while i < len(item):
            #print(i, item[i]['name'])
#           i+=1   
#        
#    artists.append(item[0]['name'])

# Eminem: spotify:playlist:5otnNgFTnMpWOFjPChrqu6 
# Drake: spotify:playlist:7b46c5syjtG86a77R7SnMs
# Lil Wayne: spotify:playlist:1zXwFGPTBcGbtV8VNYppvs
# Kanye West: spotify:playlist:3tSzoY3XPBJxWy3FFD05Bx
# Chris Brown: spotify:playlist:1it0GYp58l9RLabZUdmvOH
