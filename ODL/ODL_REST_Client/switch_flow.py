import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf

conf=conf()
def switch_flow(flow):
        
	print 'turn off'+flow['flowName']
        
	#Json confi
	headers = {'Content-type': 'application/json'}
	flowUrl = '/controller/nb/v2/flowprogrammer/default/node/OF/'+flow['switchId']+'/staticFlow/'+flow['flowName']
	url =conf['controllerIp'] + flowUrl
	#Put flow
	result=requests.post(url,auth=conf['auth'],headers=headers)
        #Print result
	print result
#Reference:http://net-ed.blogspot.se/2013/11/using-python-rest-api-to-manage-flow.html
