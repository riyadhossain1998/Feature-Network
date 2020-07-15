import os 
import sys
import json
import csv
import spotipy
import webbrowser
import re
import spotipy.util as util
import pandas as pd
from typing import List, Dict
from json.decoder import JSONDecodeError


def main():
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
        'spotify:playlist:32imPlsofSE50zCUJA1EwU'

    ]
    artist_list = ['eminem', 'drake', 'lil_wayne', 'kanye_west', 'chris_brown', 'kendrick_lamar','nicki_minaj', 'rihanna',
    'justin_bieber','juice_wrld','travis_scott','ed_sheeran','cardi_b','post_malone']
    num = 0
    total_list = []
    #getArtistData('spotify:playlist:3bhm3Oy0CZih0Sjy9IngXq','post_malone')
    while num < len(artist_list):
        # Old code or getting from multiple playlists
        #pl_length = get_pl_length(pl_ids[num])
        #print(pl_length)
        #total_list.append(pl_length)
        #artists_info = get_artists(pl_ids[num]) # Gets featuring artist info
        #track_info = get_songlist(pl_ids[num]) # HAS THE LIST OF SONGS IN THE PLAYLIST THANK GOD
        #create_csv(artist_list[num], artists_info, track_info)

        # After manipulating string and reading csv
        songs = pd.read_csv('data/'+ artist_list[num] +'_tracks.csv', encoding='cp1252')
        artists = pd.read_csv('data/ft_'+ artist_list[num] +'.csv', keep_default_na=False, encoding='cp1252') #removes nan

        tab = create_table(songs, artists)
        tab.to_csv('data1/' + artist_list[num] + '.csv')
        print(tab)
        num+=1

def get_pl_length(pl_uri: str) -> int:
    return spotifyObject.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"

    )["total"]

def get_songlist(pl_uri: str) -> List:
    pl_length = get_pl_length(pl_uri)
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
    
def get_artists(pl_uri: str) -> List[List[Dict]]:
    pl_length = get_pl_length(pl_uri)
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

def create_table(songs: List, artists: List):
    artist_track = [] #main artist of track
    featuring = []
    header=['#','Artist','Track']
    i = 0
    j = 0

    while j < len(songs['Track']):
        #Removes intro, outro, interlude 90% successful
        trk = songs['Track'][j]   
        chklist = ["intro","outro","interlude","&","ft","- ", "feat", "with"]
        for pat in chklist:
            check = re.search(pat, trk, re.IGNORECASE)
            if check!= None:
                songs['Track'][j] = trk[:check.span()[0] - 1]    
                
        
        #print(artists['Artist0'][j])
        k = 0
        temp_art='' # main artist name
        temp_track=[] # inner list with featuring artists
        #header idea
        while k < 15:
            header_item = 'Artist' + str(k)
            header.append(header_item)
            ft = artists[header_item][j]
            if ft != '':
                i=10
                v=''
                
                while ft[i] != """'""":
                    v+=ft[i]
                    i+=1
                #print(k,v)
                
                if k == 0:
                    temp_art = v
                    artist_track.append(temp_art)
                if temp_art != v: # Removes main artist from the featured list 
                    temp_track.append(v)
                v=''
        
            
            k+=1
        featuring.append(temp_track) 
        j+=1
    
    t = 0
    test = 0
    while t < len(songs):
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

    print(test,t)
    a1 = pd.DataFrame(artist_track, columns=['Artist'])
    a2 = pd.DataFrame(featuring)
    a3 = pd.DataFrame(songs, columns=['Track'])

    frames=[a1,a3,a2]
    result = pd.concat(frames,axis=1,join='outer')
    #print(result)
    return result

def create_data_csv(total: List):
    a = open('total.csv', 'w', newline='')
    writer1 = csv.writer(a)
    
    writer1.writerow(total)
    
def create_csv(dest:str, artists:List, track_info:List):
    track_file = 'data/' + dest + '_tracks.csv'
    artist_file = 'data/' + 'ft_' + dest + '.csv' 
    g = open(track_file, 'w', newline='')
    h = open(artist_file, 'w', newline='')
    count = 0
    v = 'Track'
    u = 'Artist0,Artist1,Artist2,Artist3,Artist4,Artist5,Artist6,Artist7,Artist8,Artist9,Artist10,Artist11,Artist12,Artist13,Artist14'
    writer = csv.writer(g)
    writer0 =  csv.writer(h)
    writer.writerow([v])
    #writer0.writerow([u])
    while count < len(track_info):
    
        v = track_info[count]    
        writer.writerow([v])
        writer0.writerow(artists[count])

        
        #print(count, track_info[count]) # EACH SONG
        count+=1
    
def getArtistData(pl_uri, artist_name:str):
    #total_list.append(pl_length)
    artists_info = get_artists(pl_uri) # Gets featuring artist info
    track_info = get_songlist(pl_uri) # HAS THE LIST OF SONGS IN THE PLAYLIST THANK GOD
    create_csv(artist_name,artists_info,track_info)


if __name__ == "__main__":
    main()



#create_data_csv(total_list)



# Song name, Artist, Featuring Artists, Streams, Year

# Retrieve 12 artist song list 
# Young Thug, Drake, Eminem, Travis Scott, Future, Juice WRLD, 
# Kendrick Lamar, Lil Pump, J. Cole, Akon, Lil Wayne, Lil Tecca


# Eminem: spotify:playlist:5otnNgFTnMpWOFjPChrqu6 
# Drake: spotify:playlist:7b46c5syjtG86a77R7SnMs
# Lil Wayne: spotify:playlist:1zXwFGPTBcGbtV8VNYppvs
# Kanye West: spotify:playlist:3tSzoY3XPBJxWy3FFD05Bx
# Chris Brown: spotify:playlist:1it0GYp58l9RLabZUdmvOH
