# -*- coding: utf-8 -*-
inFileClus = './idea/region/cluster'
table = 'regiontime'
T = 6 
deltaT = 0 
database = 'shanghai'

import MySQLdb
import datetime

conn=MySQLdb.connect(host="127.0.0.1",user="ywl",passwd="123456",db=database,charset="utf8")   
cursor = conn.cursor()

def timestamp(trace):
    conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")


    cursor = conn.cursor()
    time = []
    for traceItem in trace:
        path,timeST = traceItem 
        if len(path) < 3:
            time.append(timeST)
            continue
        period = timeST[0].hour/T
        t = [] 
        for i in range(1,len(path)-1):
            try:
                cursor.execute('select ref from %s where region = %s and period = %s'%(table,path[i],period))
                ref = cursor.fetchall()[0][0]
            except:
                cursor.execute('select ref from %s'%table)
                ref = cursor.fetchall()[0][0]
            info = ref.split('#')
            infotime = []
            signal = 0
            for item in info[:-1]:
                infoItem = item.split(',')
                infotime.append(float(infoItem[2]))
                if int(infoItem[0]) == path[i-1] and int(infoItem[1]) == path[i+1]:
                    t.append(float(infoItem[2]))
                    signal = 1
                    break
            if signal == 0:
                t.append(float(sum(infotime))/len(infotime))
        try:
            cursor.execute('select ref from %s where region = %s and period = %s'%(table,path[i],period))
            ref = cursor.fetchall()[0][0]
        except:
            cursor.execute('select ref from %s'%table)
            ref = cursor.fetchall()[0][0]
        info = ref.split('#')
        infotime = []
        signal = 0
        for item in info[:-1]:
            infoItem = item.split(',')
            infotime.append(float(infoItem[2]))
            if int(infoItem[0]) == path[i-1]:
                t.append(float(infoItem[2]))
                signal = 1
                break
        if signal == 0:
            t.append(float(sum(infotime))/len(infotime))
        duration = (timeST[1] - timeST[0]).seconds + deltaT
        ratio = float(duration)/sum(t)
        resultT = [timeST[0]]
        for item in t:
            resultT.append(resultT[-1] + datetime.timedelta(seconds = item * ratio))
        time.append(resultT)
    return time

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
