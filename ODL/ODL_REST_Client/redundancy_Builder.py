from flow_finder import flow_finder
from extract_redundancy import extract_redundancy
import datetime
def redundancy_Builder():
        redundancy=[]
        print 'work 1'
        input = open('redundancytable.txt', 'r')
        input.readline()
        while 1:
                print 'work'
                line=input.readline()
                if not line:
                        break
                formated_redundancy=extract_redundancy(line)
                redundancy.append(formated_redundancy)
        input.close()
        return redundancy
