def extract_flow(data):
    length= len(data)
    index=0
    flow={'flowName':'','switchId':'','inComingPort':'','actions':[''],'Status':''}
    temp=['','','','','','','','','','','','']
    i=0
    while index<length:
            if data[index]!=' ':
                temp[i]=temp[i]+data[index]
            else:
                i=i+1
            index=index+1               
    flow['flowName']=temp[0]
    flow['Status']=temp[1]
    flow['switchId']=temp[2]
    flow['inComingPort']=temp[3]
    flow['actions'][0]=temp[4]
    if i>4:      
        for j in range(i-5):
            flow['actions'].append(temp[j+5])           
    return flow
