# -*- coding: utf-8 -*-

import regionDivision
import regionMatching
import os
import datetime

piece_x = 42
piece_y = 35
infile = './trans'
outfile = './idea/region/histogram'
mapSize =    [121.2094,121.6612,31.0106,31.3278]
T = datetime.time(4)

def info(piece_x,piece_y,info_gap):
    cntttt = 0
    unitTime = T.hour * 3600 + T.minute * 60 + T.second
    totalTime = 24 * 3600
    numTime = int(totalTime / unitTime)

    numRegion = piece_x * piece_y
    record = []

    for i in range(numRegion):
        record.append([])
        for j in range(int(numTime)):
            record[i].append([])
    filelist = os.listdir(infile)
    for filename in filelist:
        fr = open(infile + '/' + filename)
        data = fr.readlines()
        fr.close()
        lastInfo = data[0].split(',')
        lastEmpty = lastInfo[1]

        for line in data[1:]:
            nowInfo = line.split(',')
            nowEmpty = nowInfo[1]
            
            if nowEmpty != lastEmpty:
                cntttt += 1
                if cntttt == 1000 :
                    print(nowInfo)
                    cntttt = 0
                if len(nowInfo[2]) <= 13:
                      continue
                nowTime = int(nowInfo[2][11:13]) * 3600 + int(nowInfo[2][14:16]) * 60 + int(nowInfo[2][17:19])
                nowLoc = map(float,nowInfo[3:5])
                state = lastEmpty + nowEmpty
                lastEmpty = nowEmpty
                region = regionMatching.regionMatching(nowLoc,piece_x,piece_y,mapSize)
                timezone = nowTime / unitTime
                record[region][int(timezone)].append(state)
                
    return record


def histogram(piece_x,piece_y,info_gap,record):
    unitTime = T.hour * 3600 + T.minute * 60 + T.minute
    totalTime = 24 * 3600
    numTime = totalTime / unitTime
    numRegion = piece_x * piece_y
    info = []
    for i in range(int(numRegion)):
        info.append([])
        for j in range(int(numTime)):
            info[i].append({1:0,0:0})
    for i in range(int(numRegion)):
        for j in range(int(numTime)):
            if record[i][j]:
                for each in record[i][j]:
                    if each == '01':
                        info[i][j][1] += 1
                    else:
                        info[i][j][0] += 1

    gapx = info_gap[0][0]
    gapy = info_gap[1][0]
    minLon = info_gap[0][2]
    minLat = info_gap[1][2]
    for i in range(int(numRegion)):

        a = i/piece_x
        b = i%piece_x
        MINLAT = a*gapy + minLat
        MAXLAT = (1+a)*gapy + minLat
        MINLON = b*gapx + minLon
        MAXLON = (1+b)*gapx + minLon
        fw = open("%s/%s_histogram"%(outfile,i),'w')
        fw.write('%s,%s\n%s,%s\n'%(MINLAT,MAXLAT,MINLON,MAXLON))
        data = []
        for j in range(int(numTime)):
      
            if info[i][j][1] != 0 or info[i][j][0]!=0:
                print(j,info[i][j][1],info[i][j][0])
            data.append('%s:%s,%s'%(j,info[i][j][1],info[i][j][0]))
        fw.write('\n'.join(data))
        fw.close()







if __name__ == '__main__':
    info_gap = regionDivision.region_d(piece_x,piece_y)
    record = info(piece_x,piece_y,info_gap)
    histogram(piece_x,piece_y,info_gap,record)




















