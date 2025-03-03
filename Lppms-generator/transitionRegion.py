# -*- coding: utf-8 -*-

piece_x = 42
piece_y = 35
inFile = './trans'
outFileTime = "./idea/region/transaction/transTime"
outFileProb = "./idea/region/transaction/transProb"
mapSize =  [121.2094,121.6612,31.0106,31.3278]

import regionDivision
import regionMatching
import os
import time

infoGap = regionDivision.region_d(piece_x,piece_y)

def regionMatch(line):
    info = line.split(',')
    location = [float(info[3]),float(info[4])]
    return regionMatching.regionMatching(location,piece_x,piece_y,mapSize)
    

def transRegionTime(piece_x,piece_y,infoGap):
   
    trans = []
    for i in range(piece_x*piece_y):
        if i==0:
            trans.append({1:0 , piece_x:0 , piece_x+1:0})
        elif i == piece_x-1:
            trans.append({piece_x-2:0 , 2*piece_x-2:0 , 2*piece_x-1:0})
        elif i == (piece_y-1)*piece_x:
            trans.append({(piece_y-2)*piece_x:0 , (piece_y-2)*piece_x+1:0 , (piece_y-1)*piece_x+1:0})
        elif i == piece_y*piece_x-1:
            trans.append({(piece_y-1)*piece_x-1:0 , (piece_y-1)*piece_x-2:0 , piece_y*piece_x-2:0})
        elif i < piece_x:
            trans.append({i-1:0 , i+1:0 , piece_x+i:0 , piece_x+i-1:0 , piece_x+i+1:0})
        elif i > (piece_y-1)*piece_x:
            trans.append({i-1:0 , i+1:0 , i-piece_x:0 , i-piece_x-1:0 , i-piece_x+1:0})
        elif i%piece_x == 0:
            trans.append({i-piece_x:0 , i-piece_x+1:0 , i+1:0 , i+piece_x:0 , i+piece_x+1:0})
        elif (i+1)%piece_x == 0:
            trans.append({i-piece_x:0 , i-piece_x-1:0 , i-1:0 , i+piece_x:0 , i+piece_x-1:0})
        else:
            trans.append({i-piece_x:0 , i-piece_x+1:0 , i+1:0 , i+piece_x:0 , i+piece_x+1:0 , i-piece_x-1:0 , i-1:0 , i+piece_x-1:0})

    fileList = os.listdir(inFile)
    for fileName in fileList:
        fr = open('%s/%s'%(inFile,fileName))
        fr.readline()
        data = fr.readlines()
        fr.close()
        data = [item for item in map(regionMatch,data) if item != -1]
        if len(data) == 0:
            break
        lastRegion = data[0]
        for regionNum in data[1:]:
            if regionNum != lastRegion:
                try:
                    trans[lastRegion][regionNum] += 1
                except:
                    pass
                lastRegion = regionNum
                    
    return trans
    
def transRegionProb(trans):
    transProb  = []
    for i,each in enumerate(trans):
        num = 0
        count = len(each)
        key = each.keys()
        for k in key:
            num += each[k]
        info = {}
        if num!= 0:
            for k in key:
                info[k] = float(each[k])/num
        else:
            for k in key:
                info[k] = 1.0/count
        transProb.append(info)
    return transProb
        
def write2File(trans,transProb):    
    resultTrans = []
    for i,each in enumerate(trans):
        line = '%s'%i
        key = each.keys()
        for k in key:
            line += ',%s:%s'%(k,each[k])
        resultTrans.append(line)
    fw = open(outFileTime,'w')
    fw.write('\n'.join(resultTrans))
    fw.close()
    
    resultProb = []
    for i,each in enumerate(transProb):
        line = '%s'%i
        key = each.keys()
        for k in key:
            line += ',%s:%s'%(k,each[k])
        resultProb.append(line)
    fw = open(outFileProb,'w')
    fw.write('\n'.join(resultProb))
    fw.close()

if __name__ == '__main__':
    t1 = time.clock()
    infoGap = regionDivision.region_d(piece_x,piece_y)
    trans = transRegionTime(piece_x,piece_y,infoGap)
    t2 = time.clock()
    print ("time finished: %s"%(t2 - t1))
    
    transProb = transRegionProb(trans)
    t3 = time.clock()
    print ("prob finished: %s"%(t3 - t2))
    
    write2File(trans,transProb)
    t4 = time.clock()
    print ("write finished: %s"%(t4 - t3))




















                   