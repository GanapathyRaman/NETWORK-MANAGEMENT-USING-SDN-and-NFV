def datarate_calculator(Byte_old,Byte_new,time_interval):
	rate=(float(Byte_new)-float(Byte_old))/time_interval
	if rate>100:
		rate=rate/1024
		datarate=str(rate)+'Mb/second'
	else:
		datarate=str(rate)+'Byte/second'
	return datarate

