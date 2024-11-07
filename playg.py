import asyncio
import time
from apis import read_audio_file
from shazamio import Shazam, Serialize
import sys
import json
import time
import os
import glob
import requests
import base64
import json


def extract_text_with_newlines(data):
    # Initialize an empty string to store the multi-line text
    multi_line_text = ""
    
    # Iterate through each item in the data list
    for item in data:
        # Extract the text field
        text = item.get("text", "")
        # Add the text with a newline character
        multi_line_text += text + "\n"
    print(multi_line_text)
    return multi_line_text


url = "https://musixmatch-lyrics-songs.p.rapidapi.com/songs/lyrics"

querystring = {"t":"Ankh Hai Bhari Bari","a":"Kumar Sanu","type":"json"}

headers = {
	"x-rapidapi-key": "8e1539527bmsh23f03950fb773c9p19b7b6jsnfd6fee6382de",
	"x-rapidapi-host": "musixmatch-lyrics-songs.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
ax = json.loads(response.text)

extract_text_with_newlines(ax)