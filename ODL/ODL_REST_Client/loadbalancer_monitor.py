import time
from time import ctime
from get_all_ports_statics import get_all_ports_statics
from check_old_switches import check_old_switches
from check_new_switches import check_new_switches
from check_ports_rate_lb import check_ports_rate_lb
from loadbalancer_Builder import loadbalancer_Builder
from loadbalancer import loadbalancer

def loadbalancer_monitor():
        time_interval=3

        print '==========================================================='
        print ctime(),'Loading the loadbalancing rules...'
        print '==========================================================='
        loadbalancers=loadbalancer_Builder()
        numoflb=len(loadbalancers)
        print ctime()+str(numoflb)+'rules Loaded!'
        print '==========================================================='

        print ctime(),'LoadBalancer working now!'
        print '========================Log================================'

        data_old=get_all_ports_statics()
        while 1:
                time.sleep(time_interval)
                data_new=get_all_ports_statics()
                result_switch={'Added Port':[],'Deleted Port':[]}
                #check_old_ports(data_old,data_new,result,time_interval)
                result_switch=check_ports_rate_lb(data_old,data_new,result_switch,time_interval,loadbalancers)
                data_old=data_new
       
if __name__ == "__main__":
        loadbalancer_monitor()
