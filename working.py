# Hello World program in Python
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import urllib







posturl = 'https://angular2train-6bcff.firebaseio.com/data/test.json'
req_data = {"brightness": "55"}
params = json.dumps(req_data).encode('utf8')
urllib.request.get_method = lambda: 'PUT'
req = urllib.request.Request(posturl, data=params,
                             headers={'content-type': 'application/json'})
req.get_method = lambda: 'PUT'                             
response = urllib.request.urlopen(req)
response = response.read().decode('utf-8')
print("Resp = "+response)



url = "https://angular2train-6bcff.firebaseio.com/data/test/brightness.json"
data3 = urlopen(url)
data3 = json.load(data3)
print ("Hello World! brightness=" + data3);
