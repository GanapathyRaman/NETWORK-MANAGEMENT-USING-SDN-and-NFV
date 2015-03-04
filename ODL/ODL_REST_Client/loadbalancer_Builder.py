from extract_loadbalancer import extract_loadbalancer
import datetime
def loadbalancer_Builder():
        loadbalancers=[]
        input = open('loadbalancertable.txt', 'r')
        input.readline()
        blankchain={'chain':'','rule_index':0,'rules':[]}
        chain=''
        while 1:
                line=input.readline()
                if not line:
                        break
                print line
                formated_loadbalancer=extract_loadbalancer(line)
                if chain=='':
					chain=formated_loadbalancer['chain']
					blankchain={'chain':'','rule_index':0,'rules':[]}
					loadbalancers.append(blankchain)
					lb_index=0
					loadbalancers[lb_index]['chain']=chain
					print blankchain
					print '======================'
					print 'work1'                        
                if chain==formated_loadbalancer['chain']:
					loadbalancers[lb_index]['rules'].append(formated_loadbalancer)								
                else:
					blankchain={'chain':'','rule_index':0,'rules':[]}
					chain=formated_loadbalancer['chain']
					loadbalancers.append(blankchain)
					lb_index=lb_index+1
					loadbalancers[lb_index]['chain']=chain
					loadbalancers[lb_index]['rules'].append(formated_loadbalancer)
                
        input.close()
        return loadbalancers
