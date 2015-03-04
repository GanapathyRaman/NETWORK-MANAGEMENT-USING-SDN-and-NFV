import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf
#from error_decoder import error_decoder

conf=conf()
def add_flow_tcp(flow):
	data={"installInHw":"true", "name":'', "node": {"id":"", "type":"OF"}, "ingressPort":"2","protocol": "6","etherType": "0x800","priority":"65535", "actions":["","","","","","","","","",""]}
	data['name']=flow['flowName']
	data['node']['id']=flow['switchId']
	data['ingressPort']=flow['inComingPort']
	data['actions']=flow['actions']
	headers = {'Content-type': 'application/json'}
	flowUrl = '/controller/nb/v2/flowprogrammer/default/node/OF/'+flow['switchId']+'/staticFlow/'+flow['flowName']
	url =conf['controllerIp']+flowUrl
	#Put flow
	result=requests.put(url,auth=conf['auth'],headers=headers,data=json.dumps(data))
	#Print result
	#print error_decoder(result.status_code)
	print result
        if result.status_code<400:
                print flow['flowName']+' added successfully '
                               
        else:
                print flow['flowName']+' can not be added '
        
	return result.status_code
#Reference:https://jenkins.opendaylight.org/controller/job/controlller-merge-hydrogen-stable/lastSuccessfulBuild/artifact/opendaylight/northbound/flowprogrammer/target/site/wsdocs/resource_FlowProgrammerNorthbound.html
#Reference:http://net-ed.blogspot.se/2013/11/using-python-rest-api-to-manage-flow.html
