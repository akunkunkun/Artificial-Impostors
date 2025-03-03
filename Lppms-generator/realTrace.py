# -*- coding: utf-8 -*-
inFile = './trans'
outFileTrace = './idea/trace/trace'
outFileTime = './idea/trace/time'
piece_x = 42
piece_y = 35
locInfo = [3.0 ,230.0 ,0.0 ,227.0]
regionInfo = [3.0, 0.0, 13.3529, 37.8333]

import os
import regionMatching
import regionDivision

info_gap = regionDivision.region_d(piece_x,piece_y)
fw1 = open(outFileTrace,'a')
fw2 = open(outFileTime,'a')
fileList = os.listdir(inFile)
for fileName in fileList:
    fr = open(inFile + '/' + fileName)
    data = fr.readlines()
    fr.close()
    trace = []
    time = []
    lastCarry = -1
    for line in data[1:]:
        try:
            info = line.split(',')
            carry = int(info[1])
            if lastCarry == 1 and carry == 0:
                p = ''
                t = ''
                location = [float(info[3]),float(info[4])]
                region = regionMatching.regionMatching(location,piece_x,piece_y,locInfo)
                if (region == 0):
                    region = 1
                if region == -1:
                    continue
                p += '%s,'%region
                t += '%s,'%info[2]
            elif carry is 0:
                location = [float(info[3]),float(info[4])]
                region = regionMatching.regionMatching(location,piece_x,piece_y,locInfo)
                if (region == 0):
                    region = 1
                if region == -1:
                    lastCarry = 1
                    continue
                p += '%s,'%region
                t += '%s,'%info[2]
            elif lastCarry == 0 and carry == 1:
                trace.append(p)
                time.append(t)
            lastCarry = carry
        except:
            pass
    for i in range(len(trace)):
        fw1.write(trace[i])
        fw1.write('\n')
        fw2.write(time[i])
        fw2.write('\n')

fw1.close()
fw2.close()
                
                
            
            
