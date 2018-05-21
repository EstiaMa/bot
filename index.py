from __future__ import print_function

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from tmdbv3api import TMDb 
from tmdbv3api import Movie

import json
import os

from flask import Flask
from flask import request
from flask import make_response

import movie_name as getMP
import movie_actor as getMA
import recommend as getRec
import actor_info as getActor
import sortby as getSort

# Flask app should start in global layout
app = Flask(__name__)

tmdb = TMDb()
tmdb.api_key = 'eb81f22e85389288369e61f7d0d0c7d5'

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ("starting processRequest...", req.get("queryResult").get("action"))
    if req.get("queryResult").get("action") == "getMoviePlot":
        result = getMP.process(req)
        return result
    elif req.get("queryResult").get("action") == "recommend-movie":
        result = getRec.process(req)
        return result
    elif req.get("queryResult").get("action") == "getMovieByActor":
        result = getMA.process(req)
        return result
    elif req.get("queryResult").get("action") == "actor-biography":
        result = getActor.process(req)
        return result
    elif req.get("queryResult").get("action") == "sortby":
        result = getSort.process(req)
        return result
    else:
	    return {}
	
@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "fulfillmentText": speech,
        "source": "apiai-movie-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
