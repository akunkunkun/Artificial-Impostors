# -*- coding: utf-8 -*-

observedNum = [2,5,8,11]
numUser = 30
inRealFile = './idea/trace/%s/input.trace-new'
inObserved = './idea/trace/%s/output-lppm-new'
outAttackFile = './idea/trace/attack file/%s'

for num in observedNum:
    print (num)
    fr = open(inObserved%num)
    observedData = fr.readlines()
    fr.close()
    fr = open(inRealFile%num)
    realData = fr.readlines()
    fr.close()
    user = 0
    resultObserved = []
    resultReal = []
    lastUserId = '0'
    fileNum = 0
    for i,item in enumerate(observedData):
        info = item.split(',')
        if len(info[2].split('|')) == num:
            userId = info[0]
            if userId != lastUserId:
                user += 1
                lastUserId = userId
            if user == numUser + 1:
                fw = open(outAttackFile%num + '/input.trace%s'%fileNum,'w')
                fw.write(''.join(resultReal))
                fw.close()
                fw = open(outAttackFile%num + '/output-lppm%s'%fileNum,'w')
                fw.write(''.join(resultObserved))
                fw.close()
                fileNum += 1
                user = 1
                resultReal = []
                resultObserved = []
            resultObserved.append('%s,'%user + info[1] + ',' + info[2])
            infoReal = realData[i].split(',')
            resultReal.append('%s,'%user + infoReal[1] + ',' + infoReal[2])
