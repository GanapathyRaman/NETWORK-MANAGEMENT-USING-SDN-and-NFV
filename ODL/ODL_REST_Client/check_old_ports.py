from find_switch import find_switch

def check_old_ports(data_old,data_new,result
    #go through every old switch
        numofoldswitches=len(data_old['portStatistics'])
        numofnewswitches=len(data_new['portStatistics'])
	for switchindex_new in range(numofnewswitches)
        
		#find the switch id of a given switch
		switchid_old=data_old['portStatistics'][switchindex_new]['node']['id']
		#find the corresponding switch index in the new data
		switch_index_new=find_switch(switchid_old,data_new)
		if switch_index=='switch removed'
			continue
        
		#find the num of ports of a specific old switch
		numofoldports=len(data_olddata['portStatistics'][switchindex_old]['portStatistic'])
		
		#go through every port of a specific old switch
		for portindex in range(numofoldports)
            #find the port Id of a given port index
			portid=data_old['portStatistics'][switchid]['portStatistic'][portindex]['nodeConnector']['id']
			#check if the port exist
			numofnewports=len(data_newdata['portStatistics'][switch_index_new]['portStatistic'])
			check_deleted_port(portid,data_new,switch_index_new,result)			
	return result
			
			
			
			
