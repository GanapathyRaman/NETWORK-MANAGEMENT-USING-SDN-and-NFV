import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf
#get connection info
conf=conf()
def get_all_ports_statics():
    #configure Json
    headers = {'Content-type': 'application/json'}
    flowUrl = '/controller/nb/v2/statistics/default/port'
    url = conf['controllerIp'] + flowUrl
    #get flow static
    result=requests.get(url,auth=conf['auth'],headers=headers)
    #print json result
    if result.status_code>210:
        print 'Json Error'
    #decode json data
    data=result.json()
    #return portStatic          
    return data


