# -*- coding: utf-8 -*-

piece_x = 42
piece_y = 35
infoLoc =  [121.2094,121.6612,31.0106,31.3278]
database = "shanghai"


def region_d(piece_x,piece_y,infoLoc= [121.2094,121.6612,31.0106,31.3278]):
    minLon,maxLon,minLat,maxLat = infoLoc
    gapx = (maxLon - minLon)/piece_x
    gapy = (maxLat - minLat)/piece_y
    return [[gapx,maxLon,minLon],[gapy,maxLat,minLat]]
    
if __name__ == '__main__':
    info_gap = region_d(piece_x,piece_y,infoLoc)
    



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


 

