from extract_rate import extract_rate
import datetime
def rate_Builder():
	loadbalancers=[]
	input = open('ratetable.txt', 'r')
	input.readline()
	while 1:
		line=input.readline()
		if not line:
				break
		formated_rate=extract_rate(line)
		loadbalancers.append(formated_rate)
	input.close()
	return loadbalancers
