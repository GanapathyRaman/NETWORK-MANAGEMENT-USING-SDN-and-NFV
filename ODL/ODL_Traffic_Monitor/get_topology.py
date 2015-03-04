import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf
#get connection info
conf=conf()
def get_topology():
    #configure Json
    headers = {'Content-type': 'application/json'}
    flowUrl ='/controller/nb/v2/topology/default/'
    url = conf['controllerIp'] + flowUrl
    #get flow static
    result=requests.get(url,auth=conf['auth'],headers=headers)
    #print json result
    
    #decode json data
    data=result.json()
    if result.status_code>250:
        print result
    return data

#len=len(data[u'portStatistic'])
#for i in range(len):
