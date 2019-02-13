a='''
113.2666012,23.13095325 ; 113.267267567,23.1307278911
113.260546667,23.134045 ; 113.258749788,23.1358223084

'''


# Return distance (km) between two coordinates (lng, lat)
# zhaorenyu@diditaxi.com.cn
# Jun 2015

import math

earth_radius=6378.137
SHOW_EST = False

def rad(d):
    return d * math.pi / 180.0

def distance(lat1,lng1,lat2,lng2,rectify=0):
    if lat2 > 180:
        lat2 /= 10000
    if lng2 > 180:
        lng2 /= 10000
    if lat1 > 54:
        lat1, lng1 = lng1, lat1
    if lat2 > 54:
        lat2, lng2 = lng2, lat2

    # rectify
    lat2 -= rectify
    lng2 -= rectify

    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))

    if SHOW_EST:
        print '%.6f'%lng1,'%.6f'%lat1, '%.6f'%lng2,'%.6f'%lat2,

    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s

def calc(bias):
    l=[]
    for i in a.split('\n'):
        try:
            start, end = i.split(';')
            s1,s2 = [float(j.strip()) for j in start.split(',')]
            e1,e2 = [float(j.strip()) for j in end.split(',')]
        except:
            #print i
            continue
        if e1==0:
            continue
        d = distance(s1,s2,e1,e2,bias)*1000
        if d<500:
            l.append(d)
            if SHOW_EST:
                print '%.1f'%d, 'm'
    l = sorted(l)
    ln = len(l)
    print sum(l)/ln,l[ln/2],l[ln*4/5]#,[int(i) for i in l].index(51)/float(ln)
    #print [i for i in l if i>49.99 and i<50.01]

def main():
    for bias in range(-1,0):
    #for bias in range(1,2):
        b=bias*0.00005
        print b,
        calc(b)

if __name__ == '__main__':
    main()