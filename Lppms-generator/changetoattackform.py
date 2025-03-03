# -*- coding: utf-8 -*-

outFile = './idea/attack'
clusterFile = './idea/region/cluster'
piece_x = 42
piece_y = 35

def locations():
    coordinate = []
    for i in range(piece_y):
        for j in range(piece_x):
            coordinate.append('%s,%s'%(j+1,i+1))
    fw = open('%s/locations'%outFile,'w')
    fw.write('\n'.join(coordinate))
    fw.close()
    
def mobility():
    mobility = []
    for i in range(piece_x * piece_y):
        info = '1'
        for j in range(piece_x * piece_y - 1):
            info += ',1'
        mobility.append(info)
    fw = open('%s/input.mobility'%outFile,'w')
    fw.write('\n'.join(mobility))
    fw.close()
    
def cluster():
    fr = open(clusterFile)
    c = fr.readlines()
    fr.close()
    c = map(int,c)
    maxCluster = max(c)
    minCluster = min(c)
    cluster = {}
    for i in range(minCluster,maxCluster + 1):
        cluster[i] = ''
    for i,item in enumerate(c):
        cluster[item] += '%s,'%i
    fw = open('%s/locations.clusters'%outFile,'w')
    for i in range(minCluster,maxCluster + 1):
        fw.write('%s\n'%cluster[i][:-1])
    fw.close()
    
if __name__ == '__main__':
    locations()
    mobility()
    cluster()
        
    
   
































 