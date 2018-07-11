# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import urllib

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

# https://mynewbranch-weather.herokuapp.com/webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    json.dumps(req, indent=4)

    if req.get("result").get("action") == "yahooWeatherForecast":
        res = processRequest(req)

    if req.get("result").get("action") == "getBrightness":
        res = getBrightness(req)

    if req.get("result").get("action") == "setBrightness":
        res = setBrightness(req)        
    
	if req.get("result").get("action") == "getUserInfo":
        res = setBrightness(req) 

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def getUserInfo(req):
    #data3 = "Hello WOrld!!!" #urlopen("https://angular2train-6bcff.firebaseio.com/data/test/who.json").read()
    
    turl = "https://dominospizza-78e07.firebaseio.com/users.json"
    brightness = urlopen(turl)
    brightness = json.load(brightness)
    print ("Hello World! brightness=" + str(brightness))

    speech = "user details is "+brightness
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def setBrightness(req):

    
    result = req.get("result")
    parameters = result.get("parameters")
    brightness = str(parameters.get("brightness"))

    posturl = 'https://angular2train-6bcff.firebaseio.com/data/test.json'
    req_data = {"brightness": brightness}
    params = json.dumps(req_data).encode('utf8')
    urllib.request.get_method = lambda: 'PUT'
    req = urllib.request.Request(posturl, data=params, headers={'content-type': 'application/json'})
    req.get_method = lambda: 'PUT'
    urllib.request.urlopen(req)
    
    

    speech = "Brightness in now set to "+brightness
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def getBrightness(req):
    #data3 = "Hello WOrld!!!" #urlopen("https://angular2train-6bcff.firebaseio.com/data/test/who.json").read()
    
    turl = "https://angular2train-6bcff.firebaseio.com/data/test/brightness.json"
    brightness = urlopen(turl)
    brightness = json.load(brightness)
    print ("Hello World! brightness=" + str(brightness))

    speech = "Current brightness is "+brightness
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


def processRequest(req):
    
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()



    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    #data3 = "Hello WOrld!!!" #urlopen("https://angular2train-6bcff.firebaseio.com/data/test/who.json").read()
    brightness = urlopen("https://angular2train-6bcff.firebaseio.com/data/test/brightness.json")
    brightness = json.load(brightness)

    speech = "brightness="+brightness+". Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample2"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
