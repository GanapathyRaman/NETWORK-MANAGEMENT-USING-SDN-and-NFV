def result=check_deleted_port(switchid_old,portid,data_new,numofnewports,switch_index_new,result):

	for i in range(numofnewports):
		if portid==data_new['portStatistics'][switch_index_new]['portStatistic'][i]['nodeConnector']['id']:
			break
		else:
			result['Deleted Port'].append(str(switchid_old)+':'+portid)
			print 'port removed:   '+str(switchid_old)+':'+portid 
