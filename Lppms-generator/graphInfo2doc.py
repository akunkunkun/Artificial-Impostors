# -*- coding: utf-8 -*-

outFile = './idea/graphRegion'
piece_x = 42
piece_y = 35
table = 'transregion'
database = 'shanghai'

import MySQLdb

def clean(item):
    item = map(str,item)
    return '%s,%s,%s'%(item[0],item[1],item[2]) 

conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")   
cursor = conn.cursor()

cursor.execute("select * from %s"%table)
infoGraph = cursor.fetchall()

nodeNum = piece_x * piece_y
edgeNum = len(infoGraph)

infoGraph = map(clean,infoGraph)

fw = open(outFile,'a')
fw.write('%s,%s\n'%(nodeNum,edgeNum))
fw.write('\n'.join(infoGraph))
fw.close()