from __future__ import print_function

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from tmdbv3api import TMDb 
from tmdbv3api import Movie

import json
import os

tmdb = TMDb()
tmdb.api_key = 'eb81f22e85389288369e61f7d0d0c7d5'

def process(req):
    baseurl = "https://api.themoviedb.org/3/search/movie?"
    query = makeQuery(req)
    url = baseurl + urlencode({'query': query}) + "&api_key="+tmdb.api_key
    result = urlopen(url).read()
    data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data)
    print(data)
    return res
	
def makeQuery(req):
    result = req.get("result")
    parameters = req['queryResult']['parameters']
    movie_name = parameters.get("movie-name")

    if movie_name is None:
        return None
    return movie_name


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
	
    res = data['results']
    movie = res[0]
    title = movie['title']
    overview = movie['overview']
	
    speech = "Here is an overview of the movie " +title+ ": \n\n"+overview

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "source": "apiai-movie-webhook-sample"
    }