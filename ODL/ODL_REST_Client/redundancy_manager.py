import time
from time import ctime
from add_flow import add_flow
from delete_flow import delete_flow
from flow_finder import flow_finder

def redundancy_manager(tailNodeConnector,headNodeConnector,reds):

    #search if any redundancy rules hit
    for red in reds:
        if tailNodeConnector==red['tailNodeConnector']:
            if headNodeConnector==red['headNodeConnector']:
                print 'redundancy activated:',red['redundancy name']
                for flow_delete in red['Delete flows']:
                    delete_flow(flow_finder(flow_delete))

                delete_flow(flow_finder(red['Add flows'][0]))

                for flow_add in red['Add flows']:
                    add_flow(flow_finder(flow_add))
    
