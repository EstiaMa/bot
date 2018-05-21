from __future__ import print_function

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from tmdbv3api import TMDb 
from tmdbv3api import Movie
from tmdbv3api import Person

import json
import os

tmdb = TMDb()
tmdb.api_key = 'eb81f22e85389288369e61f7d0d0c7d5'

def process(req):
    baseurl = "https://api.themoviedb.org/3/search/person?"
    query = makeQuery(req)
    url = baseurl + urlencode({'query': query}) + "&api_key="+tmdb.api_key+"&append_to_response=credits"
    result = urlopen(url).read()
    data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data)
    return res
	
def makeQuery(req):
    result = req.get("result")
    parameters = req['queryResult']['parameters']
    actor = parameters.get("actor")

    if actor is None:
        return None
    return actor


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    
    res = data['results']
    result=res[0]
    id = result['id']
    person = Person()
    p = person.details(id)
	
    speech = "Here is a short biography of " +p.name+ ": \n\n"+p.biography
    

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "source": "apiai-movie-webhook-sample"
    }