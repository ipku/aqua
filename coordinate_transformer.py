# Jun 2015, by Roi
# GCJ-02 known as Mars Geodetic System, Baidu Coordinates known as BD-09

import math

class EvilTransform():
    pi = 3.14159265358979324
    # self.a = 6378245.0, 1/f = 298.3
    # b = self.a * (1 - f)
    # self.ee = (a^2 - b^2) / a^2
    a = 6378245.0
    ee = 0.00669342162296594323


    def outOfChina(self, lat, lon):
        if (lon < 72.004 or lon > 137.8347):
            return True
        if (lat < 0.8293 or lat > 55.8271):
            return True
        return False

    def transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.pi) + 20.0 * math.sin(2.0 * x * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * self.pi) + 40.0 * math.sin(y / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * self.pi) + 320 * math.sin(y * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformLon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.pi) + 20.0 * math.sin(2.0 * x * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * self.pi) + 40.0 * math.sin(x / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * self.pi) + 300.0 * math.sin(x / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def transform(self, lat, lon):
        if self.outOfChina(lat, lon):
            return lat, lon
        dLat = self.transformLat(lon - 105.0, lat - 35.0);
        dLon = self.transformLon(lon - 105.0, lat - 35.0);
        radLat = lat / 180.0 * self.pi;
        magic = math.sin(radLat);
        magic = 1 - self.ee * magic * magic;
        sqrtMagic = math.sqrt(magic);
        dLat = (dLat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtMagic) * self.pi);
        dLon = (dLon * 180.0) / (self.a / sqrtMagic * math.cos(radLat) * self.pi);
        mgLat = lat + dLat;
        mgLon = lon + dLon;
        return mgLat, mgLon

    #
    # World Geodetic System ==> Mars Geodetic System
    def transform_wgs2mars(self, wgLat, wgLon):
        if self.outOfChina(wgLat, wgLon):
            return wgLat, wgLon
        dLat = self.transformLat(wgLon - 105.0, wgLat - 35.0)
        dLon = self.transformLon(wgLon - 105.0, wgLat - 35.0)
        radLat = wgLat / 180.0 * self.pi
        magic = math.sin(radLat)
        magic = 1 - self.ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtMagic) * self.pi)
        dLon = (dLon * 180.0) / (self.a / sqrtMagic * math.cos(radLat) * self.pi)
        mgLat = wgLat + dLat
        mgLon = wgLon + dLon
        return mgLat, mgLon

    def transform_mars2wgs(self, lat, lon):
        x, y= self.transform(lat, lon)
        lontitude = lon * 2 - y
        latitude = lat * 2 - x
        return latitude, lontitude

    def transform_mars2baidu(self, gg_lat, gg_lon):
        x = gg_lon
        y = gg_lat
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * self.pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * self.pi)
        bd_lon = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return bd_lat, bd_lon

    def transform_baidu2mars(self, bd_lat, bd_lon):
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.pi)
        thetself.a = math.atan2(y, x) - 0.000003 * math.cos(x * self.pi)
        gg_lon = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return gg_lat, gg_lon

    def transform_baidu2wgs(self, bd_lat, bd_lon):

        gcj_lat, gcj_lon = self.transform_baidu2mars(bd_lat, bd_lon)
        map84 = self.transform_mars2wgs(gcj_lat, gcj_lon)
        return map84

    def transform_wgs2baidu(self, wg_lat, wg_lon):

        gcj_lat, gcj_lon = self.transform_wgs2mars(wg_lat, wg_lon)
        bd09 = self.transform_mars2baidu(gcj_lat, gcj_lon)
        return bd09

def main():
    y, x = 113.794068, 22.678840999999998
    Tr = EvilTransform()
    print x,y
    print Tr.transform_mars2wgs(x,y)

if __name__ == '__main__':
    main()