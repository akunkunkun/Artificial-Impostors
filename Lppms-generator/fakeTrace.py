# -*- coding: utf-8 -*-
piece_x = 42
piece_y = 35
num = 10 
K = 2 
database = 'shanghai'
inFileClus = './idea/region/cluster'
inFileGraph = "./idea/graphRegion"

import MySQLdb
import time
import math
import numpy
import Queue
from collections import deque

conn=MySQLdb.connect(host='127.0.0.1',user="ywl",passwd="123456",db=database,charset="utf8")
cursor = conn.cursor()


class kdq:
    def __init__(self,v,lenth,nextV):
        self.v = v
        self.lenth = lenth
        self.nextV = nextV
        
class a_star:
    def __init__(self,v,lenth,trace,dis):
        self.v = v
        self.lenth = lenth
        self.trace = trace
        self.priority = lenth + dis[v]
    def __cmp__(self,other):
        return cmp (self.priority,other.priority)

def graphInit(n,m,head,rehead,edge,reedge):
    for i in range(n+1):
        head.append(-1)
        rehead.append(-1)
    for i in range(m+1):
        node1 = kdq(0,0,0)
        edge.append(node1)
        node2 = kdq(1,1,1)
        reedge.append(node2)
    return [head,rehead,edge,reedge]
        
def disInit(n,ans,dis,visit):
    for i in range(n+1):
        dis.append(numpy.inf)
        visit.append(0)
        ans.append(0)
    return [ans,dis,visit]
        
def insert(u,v,lenth,num,renum,head,rehead,edge,reedge):
 
    edge[num].v = v
    edge[num].lenth = lenth
    edge[num].nextV = head[u]
    head[u] = num
    num += 1
    reedge[renum].v = u
    reedge[renum].lenth = lenth
    reedge[renum].nextV = rehead[v]
    rehead[v] = renum
    renum += 1
    return [num,renum,head,rehead,edge,reedge]

def spfa(n,T,ans,dis,visit,head,rehead,edge,reedge):
    qe = [0 for i in range(n*100)]
    num = 0
    cnt = 0
    dis[T] = 0
    visit[T] = 1
    qe[num] = T
    num += 1
    
    while(num > cnt):
        temp = qe[cnt]
        cnt += 1
        visit[temp] = 0
        i = rehead[temp]
        while(i != -1):
            tt = reedge[i].v
            ttt = reedge[i].lenth
            if dis[tt] > dis[temp] + ttt:
                dis[tt] = dis[temp] + ttt
                if visit[tt] == 0:
                    qe[num] = tt
                    num += 1
                    visit[tt] = 1
            i = reedge[i].nextV
    return [ans,dis]

def A_star(S,T,K,ans,dis,head,rehead,edge,reedge):
    if S == T:
        K += 1
    if dis[S] == numpy.inf:
        result = a_star(0,-1,deque(),dis)
        return result
    queue = deque()
    queue.append(S)
    n1 = a_star(S,0,queue,dis)
    q = Queue.PriorityQueue()
    q.put(n1)
    while(not q.empty()):
        temp = q.get()
        ans[temp.v] += 1
        if ans[T] == K:
            return temp
        if ans[temp.v] > K:
            continue
        i = head[temp.v]
        while(i!=-1):
            queue = deque([item for item in temp.trace])
            queue.append(edge[i].v)
            n2 = a_star(edge[i].v,edge[i].lenth+temp.lenth,queue,dis)
            q.put(n2)
            i = edge[i].nextV
    result = a_star(0,-1,deque(),dis)
    return result

def findPath(target):
 
    fr = open(inFileGraph)
    data = fr.readlines()
    fr.close()
    info = data[0].split(',')
    n,m = [int(info[0]),int(info[1])]
    head = []
    rehead = []
    edge = []
    reedge = []
    head,rehead,edge,reedge = graphInit(n,m,head,rehead,edge,reedge)
    num = 1
    renum = 1
    for line in data[1:]:
        info = line.split(',')
        a,b,s = [int(info[0]),int(info[1]),float(info[2])]
        num,renum,head,rehead,edge,reedge = insert(a,b,s,num,renum,head,rehead,edge,reedge)
    
    fakeTrace = []
    for each in target:
        S,T,K = each
        ans = []
        dis = []
        visit = []
        ans,dis,visit = disInit(n,ans,dis,visit)
        ans,dis = spfa(n,T,ans,dis,visit,head,rehead,edge,reedge)
        result = A_star(S,T,K,ans,dis,head,rehead,edge,reedge)
        ft = []
        for item in result.trace:
            ft.append(item)
        fakeTrace.append(ft)
    return fakeTrace

def STReplace(realTrace,num):
    regionS = realTrace[0]
    regionT = realTrace[-1]
    fr = open(inFileClus)
    data = fr.readlines()
    fr.close()
    
    clusterS = int(data[regionS])
    clusterT = int(data[regionT])
    region = {clusterS:[],clusterT:[]}
    for i,each in enumerate(data):
        if int(each) in region:
            region[int(each)].append(i)
  
    x1 = regionS%piece_x
    y1 = regionS/piece_x
    x2 = regionT%piece_x
    y2 = regionT/piece_x
    disReal = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    region[clusterS].remove(regionS)
    try:
        region[clusterT].remove(regionT)
    except:
        pass
    try:
        region[clusterS].remove(regionT)
    except:
        pass
    try:
        region[clusterT].remove(regionS)
    except:
        pass
    dis = {}

    for itemS in region[clusterS]:
        x1 = itemS%piece_x
        y1 = itemS/piece_x
        for itemT in region[clusterT]:
            x2 = itemT%piece_x
            y2 = itemT/piece_x
            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            key = abs(distance - disReal)
            try:
                dis[key].append([itemS,itemT])
            except:
                dis[key] = [[itemS,itemT]]       

    disSort = dis.keys()
    disSort.sort()
    n = min([len(disSort),num])
    fakeST = []
    i = 0
    while n > 0:
        for j in dis[disSort[i]]:
            fakeST.append(j)
            n -= 1
            if n == 0:
                break
        i += 1
    return fakeST
    
def fillInPath(fakeST):
    
    for item in fakeST:
        item.append(K)
    result = findPath(fakeST)
    
    return result  
    
def fakeTrace(realTrace,num):
    fakeST = STReplace(realTrace,num)
    faketrace = fillInPath(fakeST)
    return faketrace
    
if __name__ == '__main__':
    realTrace = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
    t1 = time.clock()
    fakeST = STReplace(realTrace,num)
    if len(realTrace) == 1:
        print (fakeST)
    else:
        t2 = time.clock()
        print ('STReplace compelete: %s'%(t2-t1))
        faketrace = fillInPath(fakeST)
        t3 = time.clock()
        print ('fillInPath complete: %s'%(t3-t2))
        print (faketrace)


