from Traffic_Monitor import *
from Tkinter import *
import tkFont


class TM_Window(object):

        def start_button(self):
                self.TM.refresh([])
        def stop_button(self):
                self.TM.refresh_index=0
        
        def __init__(self):
                self.Top=Tk(className='Opendaylight Traffic Monitor')
                self.Top.resizable(False, False)
                #font
                font1 = tkFont.Font(family = 'Times New Roman',size = 20,weight =tkFont.BOLD)
                font2 = tkFont.Font(family = 'Times New Roman',size = 10)
                #Button Frame
                self.frame_button=Frame(self.Top)
                self.frame_button.pack(ipadx = 20,ipady = 20)
                #
                self.label = Label(self.Top,text='Before you click the start Button, make sure you ODL and Mininet is running.',font=font2)
                self.label.pack(side=TOP)
                #add buttons
                
                self.button = Button(self.frame_button,width=30,padx=5,pady=2,font=font2)
                self.button['text'] = 'Start'
                self.button['bd']=6
                self.button['command'] =self.start_button
                
                self.button.pack(side=LEFT,padx = 20,pady = 20)

                self.button = Button(self.frame_button,width=30,padx=5,pady=2,font=font2)
                self.button['text'] = 'Stop'
                self.button['bd']=6
                self.button['command'] =self.stop_button
                
                self.button.pack(side=LEFT,padx = 20,pady = 20)
                
                #Topo
                self.TM=spg_topo(self.Top)
                self.Top.mainloop()
