from redundancy_manager import redundancy_manager
from recovery_manager import recovery_manager
import thread

def check_topo(data_orgi,data_old_o,data_new,result_topo_deleted,reds):
    data_old=data_orgi
    num_of_new_links=len(data_new['edgeProperties'])
    num_of_old_links=len(data_old['edgeProperties'])
    for link_index_old in range(num_of_old_links):
        switch_id_old=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['node']['id']
        flag=0
        for link_index_new in range(num_of_new_links):
            if switch_id_old==data_new['edgeProperties'][link_index_new]['edge']['headNodeConnector']['node']['id']:
                port_id_old=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['id']
                if port_id_old==data_new['edgeProperties'][link_index_new]['edge']['headNodeConnector']['id']:
                    switch_id_old_2=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['node']['id']
                    if switch_id_old_2==data_new['edgeProperties'][link_index_new]['edge']['tailNodeConnector']['node']['id']:
                        port_id_old_2=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['id']
                        if port_id_old_2==data_new['edgeProperties'][link_index_new]['edge']['tailNodeConnector']['id']:
                            flag=1
                            break
        if flag==0:
            s1=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['node']['id'] #switch ID
            p1=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['id'] #Port ID
            s2=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['node']['id'] #switch ID
            p2=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['id'] #Port ID

            result_topo_deleted['headNodeConnector'].append(s1)
            result_topo_deleted['hn port'].append(p1)
            result_topo_deleted['tailNodeConnector'].append(s2)
            result_topo_deleted['tn port'].append(p2)
            print 'Link Removed',' Switch ',s1,' port ',p1,' --- ',' Switch ',s2,' port ',p2
            redundancy_manager(s2,s1,reds)

    data_old=data_old_o
    temp=data_old
    data_old=data_new
    data_new=temp
    num_of_new_links=len(data_new['edgeProperties'])
    num_of_old_links=len(data_old['edgeProperties'])
	
    for link_index_old in range(num_of_old_links):
        switch_id_old=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['node']['id']
        flag=0
        for link_index_new in range(num_of_new_links):
            if switch_id_old==data_new['edgeProperties'][link_index_new]['edge']['headNodeConnector']['node']['id']:
                port_id_old=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['id']
                if port_id_old==data_new['edgeProperties'][link_index_new]['edge']['headNodeConnector']['id']:
                    switch_id_old_2=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['node']['id']
                    if switch_id_old_2==data_new['edgeProperties'][link_index_new]['edge']['tailNodeConnector']['node']['id']:
                        port_id_old_2=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['id']
                        if port_id_old_2==data_new['edgeProperties'][link_index_new]['edge']['tailNodeConnector']['id']:
                            flag=1
                            break
        if flag==0:
            s1=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['node']['id'] #switch ID
            p1=data_old['edgeProperties'][link_index_old]['edge']['tailNodeConnector']['id'] #Port ID
            s2=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['node']['id'] #switch ID
            p2=data_old['edgeProperties'][link_index_old]['edge']['headNodeConnector']['id'] #Port ID

            result_topo_deleted['headNodeConnector'].append(s1)
            result_topo_deleted['hn port'].append(p1)
            result_topo_deleted['tailNodeConnector'].append(s2)
            result_topo_deleted['tn port'].append(p2)
            print 'A failure link recovered',' Switch ',s1,' port ',p1,' --- ',' Switch ',s2,' port ',p2
            recovery_manager(s2,s1,reds)
			
    return result_topo_deleted

