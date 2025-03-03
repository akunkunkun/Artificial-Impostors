# -*- coding: utf-8 -*
inFile = './idea/region/histogram'
database = 'shanghai'

import MySQLdb
import distance
import os
from math import radians, cos, sin, asin, sqrt
r = 6371

def distance(lon1, lat1, lon2, lat2):

    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * r * 1000

fileList = os.listdir(inFile)
region = []
for i in range(len(fileList)):
    region.append(0)
for filename in fileList:
    fr = open(inFile + '/' + filename)
    info1 = map(float,fr.readline().split(','))
    info2 = map(float,fr.readline().split(','))
    fr.close()
    lat = sum(info1)/2
    lon = sum(info2)/2
    regionID = int(filename[:-10])
    region[regionID] = [lon,lat]
    
conn=MySQLdb.connect(host="127.0.0.1",user="ywl",passwd="123456",db=database,charset="utf8")   
cursor = conn.cursor()

for i in range(len(region)-1):
    regionInfo1 = region[i]
    for j in range(len(region[i+1:])):
        regionInfo2 = region[i+j+1]
        dis = distance(regionInfo1[0],regionInfo1[1],regionInfo2[0],regionInfo2[1])
        cursor.execute("insert into regiondistance values('%s','%s','%s')"%(i,i+j+1,dis))
        
conn.commit()
cursor.close()
conn.close()
    
