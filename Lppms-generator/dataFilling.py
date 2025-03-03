# -*- coding: utf-8 -*-

inFile = "./idea/region/histogram"
outFile = "./idea/region/histogramFill"
piece_x = 42
piece_y = 35
thre_cluster = 0.03
thre_fill = 10
database = "shanghai"
table = "regionedgefill"

import MySQLdb
import scipy.cluster.hierarchy as sch
import scipy

def compute(data):
    result = data[0]
    for each in data[1:]:
        for i in range(len(result)):
            result[i][0] += each[i][0]
            result[i][1] += each[i][1]

    num = len(data)
    for i in range(len(result)):
        result[i][0] = float(result[i][0])/num
        result[i][1] = float(result[i][1])/num
    return result

def cluster():
    conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")

    cursor = conn.cursor()
    cursor.execute('select * from %s'%table)
    data = cursor.fetchall()
    region = []
    regionNum = piece_x * piece_y
    for i in range(regionNum * (regionNum-1) / 2):
        region.append(0)
    for item in data:
        x = int(item[0])
        y = int(item[1])
        similarity = 1.0 / (float(item[2]) + 0.00001)
        if x < y:
            index = x*regionNum + y - (x*(3+x))/2 - 1
            region[index] = similarity

    disMat = scipy.array(region)
    
    Z=sch.linkage(disMat,method='average') 
    cluster= sch.fcluster(Z, thre_cluster, 'inconsistent')
    return cluster
    
def fill(needFillRegion):
   
    for region in needFillRegion:
        if region == 0:
            regionAround = [1,piece_x,piece_x+1]
        elif region == piece_x-1:
            regionAround = [piece_x-2,2*piece_x-2,2*piece_x-1]
        elif region == (piece_y-1)*piece_x:
            regionAround = [(piece_y-2)*piece_x,(piece_y-2)*piece_x+1,(piece_y-1)*piece_x+1]
        elif region == piece_y*piece_x-1:
            regionAround = [(piece_y-1)*piece_x-1,(piece_y-1)*piece_x-2,piece_y*piece_x-2]
        elif region < piece_x:
            regionAround = [region-1,region+1,piece_x+region,piece_x+region-1,piece_x+region+1]
        elif region > (piece_y-1)*piece_x:
            regionAround = [region-1,region+1,region-piece_x,region-piece_x-1,region-piece_x+1]
        elif region%piece_x == 0:
            regionAround = [region-piece_x,region-piece_x+1,region+1,region+piece_x,region+piece_x+1]
        elif (region+1)%piece_x == 0:
            regionAround = [region-piece_x,region-piece_x-1,region-1,region+piece_x,region+piece_x-1]
        else:
            regionAround = [region-piece_x,region-piece_x+1,region+1,region+piece_x,region+piece_x+1,region-piece_x-1,region-1,region+piece_x-1]
        
        histogramSelf = []
        fr = open(inFile + '/%s_histogram'%region)
        data = fr.readlines()
        fr.close()
        regionInfo = "%s%s"%(data[0],data[1])
        for each in data[2:]:
            info = map(float,each.split(':')[1].split(','))
            histogramSelf.append(info)
            
        histogramOthers = []
        for r in regionAround:
            fr = open(inFile + '/%s_histogram'%r)
            data = fr.readlines()
            fr.close()
            histogramInfo = []
            for each in data[2:]:
                info = map(float,each.split(':')[1].split(','))
                histogramInfo.append(info)
            histogramOthers.append(histogramInfo)
        
        resultOthers = compute(histogramOthers)
        result = compute([histogramSelf,resultOthers])
        for i in range(len(result)):
            regionInfo += '%s:%s,%s\n'%(i,result[i][0],result[i][1])
        fw = open(outFile + '/%s_histogram'%region,'w')
        fw.write(regionInfo[:-1])
        fw.close()
        
            

    
if __name__ == '__main__':
    
    cluster = cluster()
    infoCluster = []
    
    numCluster = max(cluster)
    for i in range(1,numCluster + 1):
        infoCluster.append(len([item for item in cluster if item == i]))
    
    needFillCluster = []
    for i in range(numCluster):
        if infoCluster[i] < thre_cluster:
            needFillCluster.append(i+1)
            
    needFillRegion = []
    for region in range(len(cluster)):
        if cluster[region] in needFillCluster:
            needFillRegion.append(region)
    print(needFillRegion)
    fill(needFillRegion)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        