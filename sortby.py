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
    sort = parameters.get("sort")
    order = parameters.get("order")

    global kind
	
    if type is None or sort is None:
        return None
		
    if "movie" in type or "film" in type:
        type = "movie"
    elif "tv" in type or "series" in type or "show" in type:
        type = "tv"
        kind = "tv"
    else:
        type = "movie"
		
    if "least" in order:
        order = ".asc"
    else:
        order = ".desc"

    if "popular" in sort or "famous" in sort:
        sort = "popular"
    elif "recent" in sort or "latest" in sort or "newest" in sort:
        sort = "release_date"
    elif "oldest" in sort:
        sort = "release_date"
        order = ".asc"
    elif "voted" in sort or "starred" in sort:
        sort = "vote_count"
    else:
        sort = "popular"
		
    return type +"?sort_by="+sort+order


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    res = data['results']

    text = []
    text.append("Here are the results you were looking for: ")
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