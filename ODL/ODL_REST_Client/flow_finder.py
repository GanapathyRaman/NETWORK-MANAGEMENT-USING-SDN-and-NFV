from extract_flow import extract_flow
def flow_finder(flowName):
    input = open('flowtable.txt')
    input.readline()
    while 1:
        line=input.readline()
        if not line:
            break
        if not line.find(flowName) == -1:
            return extract_flow(line)
            break
    input.close()   

