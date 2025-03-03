# -*- coding: utf-8 -*-

database = 'shanghai'
clusterFile = './idea/region/cluster'

regionNum = 1470
thre = 0.005 
table = 'regionedgefill'

import scipy
import scipy.cluster.hierarchy as sch
import MySQLdb
import time
import json

def hierarchical(regionNum):
  
    start = time.clock()
 
    conn=MySQLdb.connect(host="127.0.0.1",user="ywl",passwd="123456",db=database,charset="utf8")
    cursor = conn.cursor()
    cursor.execute('select * from %s'%table)
    data = cursor.fetchall()
    region = []
    for i in range(regionNum * (regionNum-1) / 2):
        region.append(0)
    for item in data:
        x = int(item[0])
        y = int(item[1])
        distance = abs(float(item[2]))
        if x < y:
            index = x*regionNum + y - (x*(3+x))/2 - 1
            region[index] = distance
    end1 = time.clock()
    print ("dataLoad finished: %s"%(end1 - start))
    
   
    disMat = scipy.array(region)
    Z=sch.linkage(disMat,method='average') 
    cluster= sch.fcluster(Z, thre, 'distance') 
    
    end2 = time.clock()
    print ("hierarchical clustering finished: %s"%(end2 - end1))
    a = map(str,cluster)
    fw = open(clusterFile,'w')
    fw.write('\n'.join(a))
    fw.close()
    
    cluster_dict = {}  
    for region_id, cluster_id in enumerate(cluster):  
        if cluster_id not in cluster_dict:  
            cluster_dict[cluster_id] = []  
        cluster_dict[cluster_id].append(region_id)  


if __name__ == '__main__':
    hierarchical(regionNum)

