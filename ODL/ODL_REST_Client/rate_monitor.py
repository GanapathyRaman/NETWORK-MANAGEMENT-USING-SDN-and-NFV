import time
from rate_Builder import rate_Builder
import sys
from get_all_ports_statics import get_all_ports_statics
from check_old_switches import check_old_switches
from check_new_switches import check_new_switches
from check_ports_rate import check_ports_rate



#default settings
mode='all'
time_interval=3

for arg in range(len(sys.argv)):
        if sys.argv[arg]=='-m':
                mode=sys.argv[arg+1]
        elif sys.argv[arg]=='-t':
                time_interval=float(sys.argv[arg+1])
if mode=='customer':
        rate=rate_Builder()
else:
        rate={}
print mode
print '==========================================================='
print 'Rate Moniting Started...'

data_old=get_all_ports_statics()
while 1:
	time.sleep(time_interval)
	data_new=get_all_ports_statics()
	result_switch={'Added Port':[],'Deleted Port':[]}
	#check_old_ports(data_old,data_new,result,time_interval)
	result_switch=check_ports_rate(data_old,data_new,result_switch,time_interval,mode,rate)
	data_old=data_new  
	
	

    #print result_switch
