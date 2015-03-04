import requests
import json
from requests.auth import HTTPBasicAuth
from conf import conf
#from error_decoder import error_decoder

conf=conf()
def delete_flow(flow):
        headers = {'Content-type': 'application/json'}
        flowUrl = '/controller/nb/v2/flowprogrammer/default/node/OF/' + flow['switchId'] + '/staticFlow/' + flow['flowName']
        url =conf['controllerIp']+flowUrl
	#Put flow
        result=requests.delete(url,auth=conf['auth'],headers=headers)
        #Print result
        #print error_decoder(result.status_code)
        print result
        if result.status_code<400:
                print flow['flowName']+' deleted successfully '                              
        else:
                print flow['flowName']+' can not be deleted '
        
        return result.status_code
#Reference:https://jenkins.opendaylight.org/controller/job/controlller-merge-hydrogen-stable/lastSuccessfulBuild/artifact/opendaylight/northbound/flowprogrammer/target/site/wsdocs/resource_FlowProgrammerNorthbound.html
#Reference:http://net-ed.blogspot.se/2013/11/using-python-rest-api-to-manage-flow.html
