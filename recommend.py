from __future__ import print_function

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from tmdbv3api import TMDb 
from tmdbv3api import Movie

import requests
import json
import os

tmdb = TMDb()
tmdb.api_key = 'eb81f22e85389288369e61f7d0d0c7d5'
kind = "movie"

def process(req):
    query = makeQuery(req)
    response = requests.get('https://api.themoviedb.org/3/discover/'+query+'&api_key='+tmdb.api_key)
    resp = response.json()
    print(resp)
    res = makeWebhookResult(resp)
    return res
	
def makeQuery(req):
    result = req.get("result")
    parameters = req['queryResult']['parameters']
    type = parameters.get("type")
    gen = parameters.get("genre")
    lang = parameters.get("language")

    global kind
	
    if type is None:
        return None
		
    if "movie" in type or "film" in type:
        type = "movie"
    elif "tv" in type or "series" in type or "show" in type:
        type = "tv"
        kind = "tv"
    else:
        type = "movie"
    
    genre = str(getGenre(gen))
		
    return type +"?with_genres="+genre

def getGenre(gen):
    response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key='+tmdb.api_key)
    resp = response.json()
	
    res = resp['genres']

    for genre in res:
        gName = genre['name']
        if (gen == gName.lower()):
            return genre['id']

    return None


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    res = data['results']

    text = []
    text.append("Here are my recommendations: ")
    for movie in res:
        if("movie" in kind):
            title = movie['title']
        else:
            title = movie['name']
			
        text.append(title+"  ")
	
    speech = '\n 	'.join(text)

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "source": "apiai-movie-webhook-sample"
    }