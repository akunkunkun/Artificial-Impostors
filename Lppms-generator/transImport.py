# -*- coding: utf-8 -*-

inFileRegion = './idea/region/transaction/transProb'
database = 'shanghai'
table = 'transregion'

import MySQLdb
import math

conn=MySQLdb.connect(host="127.0.0.1",user="ywl",passwd="123456",db=database,charset="utf8")   
cursor = conn.cursor()

def transRegion():
    fr = open(inFileRegion)
    data = fr.readlines()
    fr.close()
    for line in data:
        info = line.split(',')
        for each in info[2:]:
            item = each.split(':')
            try:
                weight = math.log(1.0/float(item[1]))
                cursor.execute("insert into %s values(%s,%s,%s)"%(table,info[0],item[0],weight))
            except:
                pass
    conn.commit()
    
if __name__ == '__main__':
    transRegion()
    