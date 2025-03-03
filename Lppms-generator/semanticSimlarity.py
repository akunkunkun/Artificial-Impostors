# -*- coding: utf-8 -*-

table = 'regionedge2'
database = 'shanghai'
infile = './idea/region/histogram'

alpha = 0.5
belta = 0.5

import MySQLdb
import math
import os
import time

def innerProduct(P,Q):
   
    lenth = len(P)
    numerator = sum([P[i] * Q[i] for i in range(lenth)])
    denominator = math.sqrt(sum([item **2 for item in P]) * sum([item **2 for item in Q]))
    return abs(1 - (float(numerator)/denominator))

def similarity(histogram,table):
  
    conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")

    cursor = conn.cursor()
    sql_node = "insert into %s values('%s','%s','%s')"
    for i,each in enumerate(histogram[:-1]):
        for j,item in enumerate(histogram[i+1:]):
            similarity = alpha*(innerProduct(each[0],item[0])) + belta*(innerProduct(each[1],item[1]))
            cursor.execute(sql_node%(table,i,i+j+1,similarity))
    conn.commit()
    cursor.close()
    conn.close()
   
def sim(table,infile):
    filelist = os.listdir(infile)
    numregion = len(filelist)
    histogram = []
    for i in range(numregion):
        histogram.append([])
    for filename in filelist:
        fr = open(infile + '/' + filename)
        data = fr.readlines()
        region = int(filename[:-10])
        numIn = []
        numOut = []
        for each in data[2:]:
            info = each.split(':')
            statistic = info[1].split(',')
            numIn.append(float(statistic[0]))
            numOut.append(float(statistic[1]))
        numberIn = sum(numIn)
        numberOut = sum(numOut)
  
        proportionIn = []
        proportionOut = []
        for x,item in enumerate(numIn):
            if item == 0:
                numIn[x] = 1
                numberIn += 1
        for item in numIn:
            proportionIn.append(float(item) / numberIn)       
        for x,item in enumerate(numOut):
            if item == 0:
                numOut[x] = 1
                numberOut += 1
        for item in numOut:
            proportionOut.append(float(item) / numberOut)
        histogram[region] = [proportionIn,proportionOut]
    similarity(histogram,table)      

if __name__ == '__main__':
    start = time.clock()
    filelist = os.listdir(infile)
    fr = open(infile + '/0_histogram')
    d = fr.readlines()
    fr.close()
    numtime = len(d) - 2
    numregion = len(filelist)
    histogram = []
    for i in range(numregion):
        histogram.append([])
    for filename in filelist:
        fr = open(infile + '/' + filename)
        data = fr.readlines()
        region = int(filename[:-10])
        numIn = []
        numOut = []
        for each in data[2:]:
            info = each.split(':')
            statistic = info[1].split(',')
            numIn.append(float(statistic[0]))
            numOut.append(float(statistic[1]))
        numberIn = sum(numIn)
        numberOut = sum(numOut)

        proportionIn = []
        proportionOut = []
        for x,item in enumerate(numIn):
            if item == 0:
                numIn[x] = 1
                numberIn += 1
        for item in numIn:
            proportionIn.append(float(item) / numberIn)       
        for x,item in enumerate(numOut):
            if item == 0:
                numOut[x] = 1
                numberOut += 1
        for item in numOut:
            proportionOut.append(float(item) / numberOut)
        histogram[region] = [proportionIn,proportionOut]
    end1 = time.clock()
    print ('histogram step finished: %s'%(end1 - start))
    similarity(histogram,table)
    end2 = time.clock()
    print ('similarity step finished: %s'%(end2 - end1))
        
        






































