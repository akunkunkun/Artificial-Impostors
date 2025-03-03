# -*- coding: utf-8 -*-

piece_x = 42
piece_y = 35
mapSize =  [121.2094,121.6612,31.0106,31.3278]

def regionMatching(location,piece_x,piece_y,mapSize):

    lon,lat = location
    minLon, maxLon, minLat, maxLat = mapSize
    gapx = (maxLon - minLon) / piece_x
    gapy = (maxLat - minLat) / piece_y
    if lon >= maxLon or lon <= minLon or lat >= maxLat or lat <= minLat:
        return -1
    else:
     
        x = (lon - minLon)/gapx
        y = (lat - minLat)/gapy
        number = piece_x * int(y) + int(x)
        return number




if __name__ == '__main__':

    info_gap = regionDivision.region_d(piece_x, piece_y)
    location =  [-566054.215694, -798779.526994]
    region = regionMatching(location, piece_x, info_gap)
    print (region)