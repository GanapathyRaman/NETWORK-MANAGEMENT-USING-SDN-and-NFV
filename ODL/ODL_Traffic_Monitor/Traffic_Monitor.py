from Tkinter import *
import time
import random
import thread
from get_topology import get_topology
from rate_monitor_spg import rate_monitor_spg
from get_all_ports_statics import get_all_ports_statics
from check_ports_rate_spg import check_ports_rate_spg

class switch(object):
        def __init__(self,name,cv,switch_image,x=100,y=100):
                self.name=name
                self.x=x
                self.y=y
                self.links=[]
                self.pairs=[]
                self.cv=cv
                self.image = cv.create_image(self.x,self.y,anchor=NE,image=switch_image,tags=name)
                cv.tag_bind(name,'<B1-Motion>',self.move)
                
                
        def move(self,event):
                self.cv.coords(self.image,(event.x,event.y))
                self.x=event.x
                self.y=event.y
                for index in range(len(self.links)):
                        self.links[index].move(self,self.pairs[index],self.cv)
                        
                        
        def add_link(self,s2,link):
                self.links.append(link)
                self.pairs.append(s2)

class link(object):
        def __init__(self,s1,s2,cv,port_1,port_2):
                self.cv=cv
                self.margin=27
                
                self.line=cv.create_line((s1.x-self.margin,s1.y+self.margin,s2.x-self.margin,s2.y+self.margin),width=3)
                cv.itemconfig(self.line,fill= '#20B2AA')

                self.head=s1.name
                self.head_port=port_1

                self.tail=s2.name
                self.tail_port=port_2
                print 'add link ',self.head,'port ',self.head_port,' ',self.tail,' ','port ',self.tail_port
        def move(self,s_move,s_change,cv):
                cv.coords(self.line,(s_change.x-self.margin,s_change.y+self.margin,s_move.x-self.margin,s_move.y+self.margin))

        def colorrate(self,rate):
                
                
                if rate>2000:
                        self.cv.itemconfig(self.line,fill= '#FF0033')#red
                        #print 'red'
                elif rate>1000:
                        self.cv.itemconfig(self.line,fill= '#FF9900')#yellow
                        #print 'yellow'
                elif rate>1:
                        self.cv.itemconfig(self.line,fill= '#99CC33')#green
                        #print 'green'
                else:
                        self.cv.itemconfig(self.line,fill= '#CCCCCC')#gray
                        #print 'gray'
                

def link_helper(s1,s2,cv,port_1='none',port_2='none'):
        new_link=link(s1,s2,cv,port_1,port_2)
        s1.add_link(s2,new_link)
        s2.add_link(s1,new_link)
        return new_link

def switch_finder(switches,switch_id):
        for switch in switches:
                if switch.name==switch_id:
                        
                        return switch
                        break
        
def check_new_switch(switches,switch_id):
        flag=0
        for switch in switches:
                
                if switch_id==switch.name:
                        return 1
                        break
        if flag==0:
                return 0

def check_new_link(links,switch_id_1,switch_id_2):
        flag=0
        for link in links:
                
                if switch_id_1==link.head:
                        if switch_id_2==link.tail:
                                return 1
                                break
        if flag==0:
                return 0

class spg_topo(object):
#main frame
        def __init__(self,root):

                self.root =root
                self.frame_traffic = LabelFrame(self.root,text="Traffic Visualization",font=30)
                self.frame_traffic.pack()

                self.refresh_index=1

                self.switch_image= PhotoImage(file = "switch.gif")
                
                self.height=600
                self.width=800
                self.cv = Canvas(self.frame_traffic,bg = 'white',height=self.height,width=self.width)
                                
                self.switches=[]
                self.links=[]

                self.data_old=get_all_ports_statics()

                #add switch
                                             
                self.data=get_topology()
                self.num_of_links=len(self.data['edgeProperties'])
                for index in range(self.num_of_links):
                        switch_id_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['node']['id']

                        if check_new_switch(self.switches,switch_id_1)==0:
                                new_switch_1=switch(switch_id_1,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_1)

                        switch_id_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['node']['id']
                        if check_new_switch(self.switches,switch_id_2)==0:
                                new_switch_2=switch(switch_id_2,self.cv,self.switch_image,random.randint(30,370),random.randint(30,370))
                                self.switches.append(new_switch_2)

                        if check_new_link(self.links,switch_id_1,switch_id_2)==0:
                                print 'creat link'
                                port_1=self.data['edgeProperties'][index]['edge']['headNodeConnector']['id']
                                port_2=self.data['edgeProperties'][index]['edge']['tailNodeConnector']['id']
                                new_link=link_helper(switch_finder(self.switches,switch_id_1),switch_finder(self.switches,switch_id_2),self.cv,port_1,port_2)
                                self.links.append(new_link)
                                                  
                self.cv.pack()

        def auto_triger(self):
                if self.refresh_index==1:
                        time.sleep(3)
                        self.refresh([])
                else:
                        self.refresh_index=1
                                
        def refresh(self,event):
                        print 'refresh started'

                        self.time_interval=1
                        self.mode='all'
                        #time.sleep(self.time_interval)
                        self.data_new=get_all_ports_statics()
                        self.result_switch={'Added Port':[],'Deleted Port':[]}
                        self.result_rate=[]
                        self.rates=check_ports_rate_spg(self.data_old,self.data_new,self.result_switch,self.time_interval,self.mode,self.result_rate)
                                          
                                               
                        for link in self.links:
                                head_rate=self.get_rate(self.rates,link.head,link.head_port)
                                tail_rate=self.get_rate(self.rates,link.head,link.head_port)
                                if head_rate['TX_rate']!='none':
                                        if tail_rate['RX_rate']!='none':
                                                link.colorrate(min(head_rate['TX_rate'],tail_rate['RX_rate']))
                                               
                        self.data_old=self.data_new
                        print 'relodad'
                        thread.start_new_thread(self.auto_triger,())
                        
        def get_rate(self,rates,switch_id,port_id):
                flag=0
                for rate in rates:
                        if switch_id==rate['switch_id']:
                                if port_id==rate['port_id']:
                                        flag=1
                                        return {'RX_rate':rate['RX_rate'],'TX_rate':rate['TX_rate']}
                                        break
                if flag==0:
                        return {'RX_rate':'none','TX_rate':'none'}
