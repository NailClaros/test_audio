import requests
import json
import os

key = os.environ.get('SHAZ_API_KEY')

def detect(text):
    url = "https://google-translate-api8.p.rapidapi.com/google-translate/detect/"

    querystring = {"text":f"{text}"}

    payload = {
        "key1": "value",
        "key2": "value"
    }
    headers = {
        "x-rapidapi-key": str(key),
        "x-rapidapi-host": "google-translate-api8.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.json())
    ax = json.loads(response.text)
    code = ax['result']['code']
    language = ax['result']['language']
    return code, language

def translate(text, lang):
    url = "https://google-translate-api8.p.rapidapi.com/google-translate/"

    querystring = {"text":f"{text}", "lang":f"{lang}"}

    payload = {
        "key1": "value",
        "key2": "value"
    }
    headers = {
        "x-rapidapi-key": str(key),
        "x-rapidapi-host": "google-translate-api8.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.json())
    ax = json.loads(response.text)
    
    return ax['result']

###Title
###Coverart
###natural lang
###html translation