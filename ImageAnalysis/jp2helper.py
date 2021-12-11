from osgeo import gdal
from osgeo import osr

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