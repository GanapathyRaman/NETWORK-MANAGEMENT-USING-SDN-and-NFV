import time
from time import ctime
from check_topo import check_topo
from get_topology import get_topology
from redundancy_Builder import redundancy_Builder

def topo_monitor():
    
    time_interval=0.2
    print '==========================================================='
    print ctime(),'Loading the Redundancy rules...'
    print '==========================================================='
    reds=redundancy_Builder()
    numoflb=len(reds)
    print ctime()+str(numoflb)+'Redundancy rules Loaded!'
    print '==========================================================='
    print ctime(),'Topology Monitor started'
    data_orig=get_topology()
    data_old=get_topology()
    numoflinks=len(data_orig['edgeProperties'])
    print str(numoflinks),'links detected'
    print '========================Log================================'
    for link_index_old in range(numoflinks):
        s1=data_orig['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['node']['id'] #switch ID
        p1=data_orig['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['id'] #Port ID
        s2=data_orig['edgeProperties'][link_index_old]['edge']['headNodeConnector']['node']['id'] #switch ID
        p2=data_orig['edgeProperties'][link_index_old]['edge']['headNodeConnector']['id'] #Port ID
        print' Switch ',s1,' port ',p1,' connected to ',' Switch ',s2,' port ',p2
    
    while 1:
        time.sleep(time_interval)
        data_new=get_topology()
        result_topo_deleted={'headNodeConnector':[],'hn port':[],'tailNodeConnector':[],'tn port':[]}
        result_topo_added={'headNodeConnector':[],'hn port':[],'tailNodeConnector':[],'tn port':[]}
        result_switch=check_topo(data_orig,data_old,data_new,result_topo_deleted,reds)
        data_old=data_new

    #print result_switch
if __name__ == "__main__":
    topo_monitor()

