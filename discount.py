import time
import os
import glob
import requests
import base64
import json
import sys
import io
from apis import return_lyrics, read_audio_file
from bs4 import BeautifulSoup
# Set encoding for stdout

key = os.environ.get('SHAZ_API_KEY')

def step2(full_title):
    genius_id = 0
    url = "https://shazam.p.rapidapi.com/songs/v2/detect"
    querystring = {"timezone":"America/Chicago","locale":"en-US"}
    payload = read_audio_file(full_title)
    # payload = read_audio_file(f"audio_stream/clips/clip_1.wav")
    # payload = read_audio_file("audio_stream/ex.wav")
    # payload = open('audio_stream/clinteastwood_portion_mono.txt', 'rb')
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "shazam.p.rapidapi.com",
        "Content-Type": "text/plain"
    }

    response = requests.post(url, data=payload, headers=headers, params=querystring)
    # print(response.json(), flush=True)
    # print(response.text, flush=True)
    ax = json.loads(response.text)

    #Song ID'd
    if response.status_code == 200 and "track" in ax:
        print("IN____________________ SONG FOUND")
        song_name = ax['track']['title']
        song_artist = ax['track']['subtitle']
        
        print(f'Title Name: {song_name}')
        print(f'Artist: {song_artist}')
        full_title = song_name + " " + song_artist
        print(full_title)
        if 'images' in ax['track']:
            coverart = ax['track']['images']['coverart']
        
        #look up song name for ID
        ax = return_lyrics(song_name, song_artist)
        
        if response.status_code == 200 and "hits" in ax:
                print("IN____________________ ID FOUND")
                genius_id = ax['hits'][0]['result']['id']
                print(f'Genius ID: {genius_id}')
                
                if ax['hits'][0]['result']['instrumental']:
                    print("This song is a confirmed instrumental")
                    # return 2, song_name, song_artist, "", ""
                    return 2, full_title


                url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"
                # genius_id = 115478
                querystring = {"id":str(genius_id), "text_format":"html"}
                headers = {
                    "x-rapidapi-key": str(key),
                    "x-rapidapi-host": "genius-song-lyrics1.p.rapidapi.com"
                }
                response = requests.get(url, headers=headers, params=querystring)
                # print(response.text)
                ax = json.loads(response.text)

                #Return Song Lyrics
                if response.status_code == 200 and "lyrics" in ax:
                    print("IN____________________ LYRICS FOUND")
                    print('Lyrics: \n\n')
                    lyric_check = ax['lyrics']['lyrics']['body']['html']	
                    if lyric_check:
                        if not isinstance(lyric_check, str):lyric_check = str(lyric_check)
                        print('Lyrics_after wrapper: \n\n')
                        print(lyric_check, flush=True)
                        ret_val = lyric_check
                        
                        soup = BeautifulSoup(lyric_check, features="html.parser")
                        s_txt = soup.get_text()
                        print('\n\n s_txt Lyrics: \n\n')
                        # print(s_txt, flush=True)
                        from trans import detect, translate
                        co, la = detect(s_txt[:130])
                        if co != "en":
                            print("Natural Langauage: " + la)
                            print("english Translation:\n")
                            print(translate(ret_val, "en"))
                        return 3, full_title
                        # return 3, song_name, song_artist, la, ret_val
                elif response.status_code == 200:
                    print('Error: cant find track___________________lyrics' )
             
        elif response.status_code == 200:
            print('Error: cant find track___________________Id' )
            print("Songs lyrics have not been located on the API/not recorded or song is likely an instrumental")
            return 1, full_title
            # return 1, song_name, song_artist, "", ""
           
    
    elif response.status_code == 200:
        print('Error: cant find track___________________at all' )
        time.sleep(.6)
        # return 1, "", "", "", ""
        return 0, ""
		# full_title = "Bye Bye Bye *NSYNC"




