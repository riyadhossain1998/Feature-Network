import os
from os import environ
import spotipy
import pandas as pd
import re
import webbrowser
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from typing import List, Dict
from json.decoder import JSONDecodeError

class Playlist:
    def __init__(self, pl_id, Artist):
        self.pl_id = pl_id
        self.Artist = Artist

class Artist:
    def __init__(self, name, total):
        self.name = name
        self.total = total




# Authenticate to Spotify
def authenticate(cliend_id: str, client_secret: str) -> spotipy.client.Spotify:
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=cliend_id,
            client_secret=client_secret
        )
    )

    return sp

def connectSpotify():
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
    return spotifyObject

def main():
    spotifyObject = connectSpotify()
    pl_id = 'spotify:playlist:5otnNgFTnMpWOFjPChrqu6'
    pl_ids = [
        'spotify:playlist:5otnNgFTnMpWOFjPChrqu6', 
        'spotify:playlist:7b46c5syjtG86a77R7SnMs', 
        'spotify:playlist:1zXwFGPTBcGbtV8VNYppvs', 
        'spotify:playlist:3tSzoY3XPBJxWy3FFD05Bx', 
        'spotify:playlist:1it0GYp58l9RLabZUdmvOH',
        'spotify:playlist:69lHZIoSfaMIikQBz5KMFH',
        'spotify:playlist:5wiWly0tLIIKetHVTvhf3P',
        'spotify:playlist:48IvzHbLovDHoKqLuVr6dx',
        'spotify:playlist:4eHNTlsildXyxn2BCAIYF0',
        'spotify:playlist:1gjuwzt1kS1BT8pQGOuoBv',
        'spotify:playlist:66IEIbzUtH45bJ0alxHgVh',
        'spotify:playlist:0cOXpSAeJ39MbXGVOtDOJw',
        'spotify:playlist:64fHuXoUCx2D6iD4bzRTKX',
        

    ]
    artist_list = ['eminem', 'drake', 'lil_wayne', 'kanye_west', 'chris_brown', 'kendrick_lamar','nicki_minaj', 'rihanna',
    'justin_bieber','juice_wrld','travis_scott','ed_sheeran','cardi_b']
    i = 0
    while i < len(pl_ids):
        filename = 'data1/'+ artist_list[i] + '.csv'

        pl_length = get_pl_length(pl_ids[i],spotifyObject)
        print(pl_length)
        artists_info = get_artists(pl_ids[i],spotifyObject) # Gets featuring artist info
        track_info = get_songlist(pl_ids[i],spotifyObject) # HAS THE LIST OF SONGS IN THE PLAYLIST THANK GOD
        
        #print(artists_info[0][0]['name'])
        a = create_table(track_info, artists_info)
        a.to_csv(filename)
        #.to_csv('data1/' + artist_list[num] + '.csv')
        print(a)
        i+=1

def get_pl_length(pl_uri: str, spotifyObject: spotipy) -> int:
    return spotifyObject.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"

    )["total"]

def get_artists(pl_uri: str, spotifyObject: spotipy) -> List[List[Dict]]:
    pl_length = get_pl_length(pl_uri, spotifyObject)
    artists_info = list()
    # Playlist tracks
    offset = 0

    # Only 100 songs at a time problem, loop to keep retrieving 

    while offset != pl_length:
        # Get next batch of tracks
        tracks = spotifyObject.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track.artists.name,items.track.artists.images"
        )

        

        # Get the list with info of each track from new batch and append 

        [artists_info.append(item["track"]["artists"])
            for item in tracks["items"]
            
            ]
        
        # Update offset
        offset += len(tracks["items"])
    return artists_info

def get_songlist(pl_uri: str, spotifyObject: spotipy) -> List:
    pl_length = get_pl_length(pl_uri, spotifyObject)
    songlist = []
    preview_url = []
    release_date = []
    offset = 0
    count = 0
    total = 0
    while offset != pl_length:
        # Get next batch of tracks
        

        tracks = spotifyObject.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track.name,items.track.preview_url,items.track.release_date,total"
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
            preview_url.append(tracks['items'][i]['track']['preview_url'])
            #release_date.append(tracks['items'][i]['track']['release_date'])
            i+=1
        
        #print(count,tracks['items'])
        offset += len(tracks['items'])
        count +=1
    
    return songlist

def create_table(songs: List, artists: List):
    artist_track = [] #main artist of track
    featuring = []
    i = 0
    j = 0

    while j < len(songs):
        #Removes intro, outro, interlude 90% successful
        trk = songs[j]   
        chklist = ["intro","outro","interlude","&","ft","- ", "feat", "with"]
        for pat in chklist:
            check = re.search(pat, trk, re.IGNORECASE)
            if check!= None:
                songs[j] = trk[:check.span()[0] - 1]    
                
        
        #print(artists['Artist0'][j])
        k = 0
        temp_art='' # main artist name
        temp_track=[] # inner list with featuring artists
        #header idea
        while k < len(artists[j]):
            ft = artists[j][k]['name']
            if k == 0:
                temp_art = ft
                artist_track.append(temp_art)
            if temp_art != ft: # Removes main artist from the featured list 
                temp_track.append(ft)
            
            k+=1
        featuring.append(temp_track) 
        j+=1
    
    t = len(songs)
    test = 0
    while t  < len(songs):
    #print(artist_track[t],"-",songs['Track'][t], featuring[t])
        if not featuring[t] and artist_track[t] == 'Eminem':
            #print("Solo:",songs['Track'][t]) # solos
            test+=1
        elif artist_track[t] != 'Eminem':
            #print(artist_track[t]," ft- " ,songs['Track'][t], featuring[t])   # featuring 
            test+=1
        else:
            #print('Featured',artist_track[t], featuring[t]) # featured
            test+=1
        t+=1

    #print(test,t)
    a1 = pd.DataFrame(artist_track, columns=['Artist'])
    a2 = pd.DataFrame(featuring)
    a3 = pd.DataFrame(songs, columns=['Track'])
    #a4 = pd.DataFrame(release_date, columns=['Release Date'])
    #a5 = pd.DataFrame(preview_url, columns=['Preview URL'])

    frames=[a1,a3,a2]
    #frames=[a1,a3,a4,a2,a5]
    result = pd.concat(frames,axis=1,join='outer')
    #print(result)
    return result



# String functions
def toString(input: str):
    artist = input.lower()
    wrt = ''
    for i in artist:
        if i == ' ':
            wrt += '_'
        else:
            wrt += i
    return wrt





if __name__ == "__main__":
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    # Get a Spotify authenticated instance
    sp_instance = authenticate(CLIENT_ID, CLIENT_SECRET)
    main()