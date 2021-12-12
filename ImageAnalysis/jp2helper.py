from osgeo import gdal
from osgeo import osr
import pyproj


#def pixel2coord(x, y):
#    xp = a * x + b * y + xoff
#    yp = d * x + e * y + yoff
#    return(xp, yp)

def transformWGS84FromLatLon(lat, lon):
    src = osr.SpatialReference()
    src.SetWellKnownGeogCS("WGS84")
    dataset = gdal.Open("i1.jp2", gdal.GA_ReadOnly)
    projection = dataset.GetProjection()
    dst = osr.SpatialReference(projection)
    ct = osr.CoordinateTransformation(src, dst)
    xy = ct.TransformPoint(lon, lat);
    return xy



_projections = {}


def zone(coordinates):
    if 56 <= coordinates[1] < 64 and 3 <= coordinates[0] < 12:
        return 32
    if 72 <= coordinates[1] < 84 and 0 <= coordinates[0] < 42:
        if coordinates[0] < 9:
            return 31
        elif coordinates[0] < 21:
            return 33
        elif coordinates[0] < 33:
            return 35
        return 37
    return int((coordinates[0] + 180) / 6) + 1


def letter(coordinates):
    return 'CDEFGHJKLMNPQRSTUVWXX'[int((coordinates[1] + 80) / 8)]


def project(coordinates):
    z = zone(coordinates)
    l = letter(coordinates)
    if z not in _projections:
        _projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
    x, y = _projections[z](coordinates[0], coordinates[1])
    if y < 0:
        y += 10000000
    return z, l, x, y


def unproject(z, l, x, y):
    if z not in _projections:
        _projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
    if l < 'N':
        y -= 10000000
    lng, lat = _projections[z](x, y, inverse=True)
    return (lng, lat)