# -*- coding: utf-8 -*-

import regionDivision
import regionMatching
import os
import datetime
import MySQLdb

piece_x = 42
piece_y = 35
numAll = piece_x * piece_y
inFile = './trans'

T = datetime.time(4)
database = 'shanghai'
mapSize =  [121.2094,121.6612,31.0106,31.3278]
region = []

def adjacent(piece_x,r1,r2):
    x1 = r1%piece_x
    y1 = r1/piece_x
    x2 = r2%piece_x
    y2 = r2/piece_x
    x = abs(x1 - x2)
    y = abs(y1 - y2)
    if x|y == 0:
        return 0
    elif x > 1 or y > 1:
        return 0
    else:
        return 1

for i in range(numAll):
    region.append([])
    for j in range(24/T.hour):
        region[i].append({})
    
fileList = os.listdir(inFile)
info_gap = regionDivision.region_d(piece_x,piece_y)
for fileName in fileList:
    fr = open(inFile + '/' + fileName)
    fr.readline()
    data = fr.readlines()
    fr.close()
        
    r1 = -3
    t2 = datetime.datetime.strptime('2010-1-1 14:00:00','%Y-%m-%d %H:%M:%S')
    r2 = -2
    for line in data[2:]:
        
        info = line.split(',')
        try:
            if len(info[2]) == 10:
                  continue
            time = datetime.datetime.strptime(info[2],'%Y-%m-%d %H:%M:%S')
            r = regionMatching.regionMatching([float(info[3]),float(info[4])],piece_x,piece_y,mapSize)
        except:
            r = r2
        if r == -1 or r >= numAll:
            r1 = -3
            t2 = datetime.datetime.strptime('2010-1-1 14:00:00','%Y-%m-%d %H:%M:%S')
            r2 = -2
        else:
            if r != r2 and r1 > 0 and r2 > 0 and adjacent(piece_x,r1,r2) and adjacent(piece_x,r,r2):
                periodT = t2.hour/T.hour
                try:
                    region[r2][periodT][r1][r][0] += (time - t2).seconds
                    region[r2][periodT][r1][r][1] += 1
                except:
                    region[r2][periodT][r1] = {}
                    region[r2][periodT][r1][r] = [(time - t2).seconds,1]
            if len(info[2]) == 10:
                  continue
            t2 = datetime.datetime.strptime(info[2],'%Y-%m-%d %H:%M:%S')
            r1 = r2
            r2 = r

conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")

cursor = conn.cursor()
for r,each in enumerate(region):
    for t,item in enumerate(each):
        ref = ''
        for r1 in item:
            for r3 in item[r1]:
                time = float(item[r1][r3][0])/(item[r1][r3][1])
                ref += '%s,%s,%s#'%(r1,r3,time)
        if ref:
            cursor.execute("insert into regiontime values('%s','%s','%s')"%(r,t,ref))
conn.commit()
cursor.close()
conn.close()
              
                
                        
                    



