# -*- coding: utf-8 -*-

T = 15*60
numTrace = 30000 
num = 10
inTraceFile = './idea/trace/trace'
inTimeFile = './idea/trace/time'
outInputTrace = './idea/trace/%s/input.trace-new'%(num + 1)
outObservedTrace = './idea/trace/%s/output-lppm-new'%(num + 1)

import fakeTrace
import addTimestamp
import datetime

user = 1
maxTime = 24 * 3600 / T
fw1 = open(outInputTrace,'w')
fw2 = open(outObservedTrace,'w')

def standardize(trace):

    rTime = []
    for item in trace[1]:
        t = item.hour * 3600 + item.minute * 60 + item.second
        order = t/T + 1
        rTime.append(order)
    if max(rTime) == min(rTime):
        resultTrace = [trace[0][0],trace[0][-1]]
        if rTime[0] == maxTime:
            resultTime = [rTime[0]-1,rTime[0]]
        else:
            resultTime = [rTime[0],rTime[0]+1]
    else:
        lastT = rTime[0] - 1
        resultTrace = []
        for i,item in enumerate(rTime):
            if item != lastT:
                for j in range(item - lastT):
                    resultTrace.append(trace[0][i])
                lastT = item
        resultTrace[-1] = trace[0][-1]
        resultTime = range(rTime[0],rTime[0] + len(resultTrace))
    return [resultTrace,resultTime]

def fake(realTrace):

    trace = [realTrace]
    fakeST = fakeTrace.STReplace(realTrace[0],num)
    if len(realTrace[0]) == 1:
        for item in fakeST:
            trace.append([[item[0]],realTrace[1]])
    else:
        faketrace = fakeTrace.fillInPath(fakeST)
        tS = realTrace[1][0]
        tT = realTrace[1][-1]
        parameterFakeTrace = []
        for item in faketrace:
            if item:
                parameterFakeTrace.append([item,[tS,tT]])
        fakeTime = addTimestamp.timestamp(parameterFakeTrace)
        for i in range(len(fakeTime)):
            trace.append([parameterFakeTrace[i][0],fakeTime[i]])

    resultTrace = []
    for item in trace:
        resultTrace.append(standardize(item))
    return resultTrace

def write2input(inputtrace):
    global user
    data = []
    trace,time = inputtrace
    for i in range(1,time[0]):
        data.append('%s,%s,%s'%(user,i,trace[0]))
    for i in range(len(trace)):
        data.append('%s,%s,%s'%(user,time[i],trace[i]))
    for i in range(time[-1] + 1,maxTime + 1):
        data.append('%s,%s,%s'%(user,i,trace[-1]))
    fw1.write('\n'.join(data))
    
    
def write2observed(observedtrace):
   
    global user
    data = []
    timeNum = len(observedtrace[0][1])
    for i in range(1,observedtrace[0][1][0]):
        info = '%s,%s,%s'%(user,i,observedtrace[0][0][0])
        for each in observedtrace[1:]:
            info += '|%s'%each[0][0]
        data.append(info)
    for i in range(timeNum):
        info = '%s,%s,%s'%(user,observedtrace[0][1][i],observedtrace[0][0][i])
        for each in observedtrace[1:]:
            info += '|%s'%each[0][i]
        data.append(info)
    for i in range(observedtrace[0][1][-1] + 1,maxTime + 1):
        info = '%s,%s,%s'%(user,i,observedtrace[0][0][-1])
        for each in observedtrace[1:]:
            info += '|%s'%each[0][-1]
        data.append(info)
    
    fw2.write('\n'.join(data))
    
    user += 1
    
def datetimeFormat(s):
    return datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
    
def testify(t):
    if (t.hour*3600 + t.minute*60 + t.second) % T == 0:
        return True
    
if __name__ == '__main__':
    fr1 = open(inTraceFile)
    dataTrace = fr1.readlines()
    fr1.close()
    fr2 = open(inTimeFile)
    dataTime = fr2.readlines()
    fr2.close()
    trace = []
    time = []
    number = 0
    i = 0
    while(number < numTrace):
        infoTrace = dataTrace[i].split(',')[:-1]
        infoTime = dataTime[i].split(',')[:-1]
        if infoTrace[0] != infoTrace[-1]:
            infoTimeNew = map(datetimeFormat,infoTime)
            if infoTimeNew[0].day == infoTimeNew[-1].day:            
                try:
                    x = sorted(infoTimeNew)
                    if x == infoTimeNew:
                        if infoTimeNew[0] < infoTimeNew[-1]:
                            time_new = infoTimeNew
                            trace.append(map(int,infoTrace))
                            number += 1
                    elif x[1:] == infoTimeNew[1:]:
                        if infoTimeNew[0] < infoTimeNew[-1]:
                            time_new = infoTimeNew[1:]
                            trace.append(map(int,infoTrace[1:]))
                            number += 1
                    if testify(time_new[0]):
                        time_new[0] += datetime.timedelta(seconds=1)
                    if testify(time_new[-1]):
                        time_new[-1] += datetime.timedelta(seconds=1)
                    time.append(time_new)
                except:
                    pass
                
        i += 1

    for i in range(numTrace):
        try:
            observedtrace = fake([trace[i],time[i]])
            inputtrace = standardize([trace[i],time[i]])
            write2input(inputtrace)
            fw1.write('\n')
            write2observed(observedtrace)
            fw2.write('\n')
        except:
            pass
    fw1.close()
    fw2.close()



