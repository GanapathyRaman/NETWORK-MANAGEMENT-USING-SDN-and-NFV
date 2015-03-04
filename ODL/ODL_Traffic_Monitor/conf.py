from requests.auth import HTTPBasicAuth
def conf():
    
    #change the following settings if necessary      
    controllerIp='http://127.0.0.1:8080'
    ODL_user='admin'
    ODL_password='admin'

    auth = HTTPBasicAuth(ODL_user,ODL_password)
    setting={'controllerIp':controllerIp,'auth':auth}
    return setting
