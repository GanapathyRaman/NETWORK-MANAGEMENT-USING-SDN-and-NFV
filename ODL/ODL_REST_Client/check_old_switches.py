def check_old_switches(data_old,data_new,result_switch):
    numofoldswitches=len(data_old['portStatistics'])
    numofnewswitches=len(data_new['portStatistics'])
    for switchindex in range(numofoldswitches):
        switchid=data_old['portStatistics'][switchindex]['node']['id']
        #check if a previous switch exist
        flag=1
        for i in range(numofnewswitches):
            if switchid==data_new['portStatistics'][i]['node']['id']:
                flag=0
                break
        if flag==1:
            result_switch['Deleted Switch:'].append(switchid)
            print 'Removed switch '+switchid
    return result_switch
