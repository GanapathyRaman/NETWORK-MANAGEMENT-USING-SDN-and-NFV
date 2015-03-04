def extract_rate(data):
    length= len(data)
    index=0

    Balancer={'balancerName':'balancer1','switchId':'00:00:00:1','portId':'0',}
    
    temp=['','','','','','','','','','','','']
    i=0
    while index<length:
            if data[index]!=' ':
                temp[i]=temp[i]+data[index]
            else:
                i=i+1
            index=index+1               
    Balancer['balancerName']=temp[0]
    Balancer['switchId']=temp[1]
    Balancer['portId']=temp[2]
    

    
    return Balancer



