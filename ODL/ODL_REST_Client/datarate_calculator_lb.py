def datarate_calculator_lb(Byte_old,Byte_new,time_interval):
	rate=(float(Byte_new)-float(Byte_old))/time_interval
	return rate

