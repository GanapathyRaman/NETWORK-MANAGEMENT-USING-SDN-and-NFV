def check_new_switches(data_old,data_new,result_switch):
    numofoldswitches=len(data_old['portStatistics'])
    numofnewswitches=len(data_new['portStatistics'])
    for switchindex in range(numofnewswitches):
        switchid=data_new['portStatistics'][switchindex]['node']['id']
        #check if a new switch added
        flag=0
        for i in range(numofoldswitches):
            if switchid==data_old['portStatistics'][i]['node']['id']:
                flag=1
                break
        if flag==0:
            result_switch['Added Switch:'].append((switchid))
            print 'New Switch: '+switchid
    return result_switch
