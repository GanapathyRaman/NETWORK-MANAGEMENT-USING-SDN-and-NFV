def extract_loadbalancer(data):
    length= len(data)
    index=0

    Balancer={'balancerName':'balancer1','chain':'','switchId':'00:00:00:1','portId':'0','threshhold':10,'type':'max','Delete flows':[],'Add flows':[]}
    
    temp=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    i=0
    while index<length:
            if data[index]!=' ':
                temp[i]=temp[i]+data[index]
            else:
                i=i+1
            index=index+1               
    Balancer['balancerName']=temp[0]
    Balancer['chain']=temp[1]
    Balancer['switchId']=temp[2]
    Balancer['portId']=temp[3]
    Balancer['threshhold']=temp[4]
    Balancer['type']=temp[5]

    for index_temp in range(6,i):
        if temp[index_temp]!='DELETE':
            if temp[index_temp]!='ADD':
                Balancer['Add flows'].append(temp[index_temp])
        elif temp[index_temp]=='DELETE':
            break
    for index_temp_d in range (index_temp+1,i):
        Balancer['Delete flows'].append(temp[index_temp_d])


    
    return Balancer



