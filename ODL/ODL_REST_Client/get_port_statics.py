import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf
#get connection info
conf=conf()
def get_port_statics(switchId='00:00:00:00:00:00:00:02',portId):
    #configure Json
    headers = {'Content-type': 'application/json'}
    flowUrl = '/controller/nb/v2/statistics/default/port/node/OF/'+switchId
    url = conf['controllerIp'] + flowUrl
    #get flow static
    result=requests.get(url,auth=conf['auth'],headers=headers)
    #print json result
    print result
    #decode json data
    data=result.json()
    #return portStatic
    portStatic{'portId':'','RxPk':'','TxPk'=''}

    if data[u'portStatistic'][0][u'nodeConnector'][u'id']=portId:
        portStatic['portId']=data[u'portStatistic'][0][u'nodeConnector'][u'id']
        portStatic['RxPk']=data[u'portStatistic'][0][u'receivePackets']
        portStatic['TxPk']=data[u'portStatistic'][0][u'transmitPackets']
        portStatic['RxBytes'][u'portStatistic'][i][u'receiveBytes']
        portStatic['TxBytes'][u'portStatistic'][i][u'transmitBytes']


        
    return portStatic


#len=len(data[u'portStatistic'])
#for i in range(len):
