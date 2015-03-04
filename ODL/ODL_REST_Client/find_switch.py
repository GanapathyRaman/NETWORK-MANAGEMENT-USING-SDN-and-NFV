def find_switch(switchid,data_new):
		numofswitchs_old=len(data_new['portStatistics'])
		for switchindex in range(numofswitchs_old):
                    flag=0
                    if switchid==data_new['portStatistics'][switchindex]['node']['id']:
                        return switchindex
                        flag=1
			break

                if flag==0:
                    return 'switch removed'
