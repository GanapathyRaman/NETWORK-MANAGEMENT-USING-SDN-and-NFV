def find_port(switchid_old,portid,data_new,numofnewports,switch_index_new,result):

	for new_port_index in range(numofnewports):
                flag=0
		if portid==data_new['portStatistics'][switch_index_new]['portStatistic'][new_port_index]['nodeConnector']['id']:
			return new_port_index
                        flag=1
			break
        if flag==0:
                result['Deleted Port'].append(str(switchid_old)+':'+portid)
                return 'port removed'
