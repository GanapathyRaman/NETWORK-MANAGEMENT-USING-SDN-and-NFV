from find_switch import find_switch
from find_port import find_port
from datarate_calculator_lb import datarate_calculator_lb
#from check_ports_rate_lb import check_ports_rate_lb

def check_ports_rate_spg(data_old,data_new,result,time_interval,mode,result_rate):
    #go through every old switch
        numofoldswitches=len(data_old['portStatistics'])
        numofnewswitches=len(data_new['portStatistics'])
        for switch_index_old in range(numofnewswitches):
                #find the switch id of a given switch
                switch_id_old=data_old['portStatistics'][switch_index_old]['node']['id']
                #find the corresponding switch index in the new data
                switch_index_new=find_switch(switch_id_old,data_new)
                if switch_index_new=='switch removed':
                        continue
        
		#find the num of ports of a specific old switch
                numofoldports=len(data_old['portStatistics'][switch_index_old]['portStatistic'])
		
		#go through every port of an old switch
                for port_index_old in range(numofoldports):
                #find the port Id of a given port index
                        portid=data_old['portStatistics'][switch_index_old]['portStatistic'][port_index_old]['nodeConnector']['id']
			#check if the port exist
                        numofnewports=len(data_new['portStatistics'][switch_index_new]['portStatistic'])
                        port_index_new=find_port(switch_id_old,portid,data_new,numofnewports,switch_index_new,result)
                        if port_index_new=='port removed':
                                print 'port'+portid+'removed'
                                continue
			
                        if mode=='all':
                                RX_Byte_old=data_old['portStatistics'][switch_index_old]['portStatistic'][port_index_old]['receiveBytes']
                                RX_Byte_new=data_new['portStatistics'][switch_index_new]['portStatistic'][port_index_new]['receiveBytes']
                                TX_Byte_old=data_old['portStatistics'][switch_index_old]['portStatistic'][port_index_old]['transmitBytes']
                                TX_Byte_new=data_new['portStatistics'][switch_index_new]['portStatistic'][port_index_new]['transmitBytes']
                                RX_rate=datarate_calculator_lb(RX_Byte_old,RX_Byte_new,time_interval)
                                TX_rate=datarate_calculator_lb(TX_Byte_old,TX_Byte_new,time_interval)
                                
                                new_rate={'switch_id':switch_id_old,'port_id':portid,'RX_rate':RX_rate,'TX_rate':TX_rate}
                                result_rate.append(new_rate)
        return result_rate
			
			
			
			
