import json
from glob import glob
from sentinelsat.sentinel import SentinelAPI
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from osgeo import gdal
from osgeo import osr
import geopandas as gpd
import rasterio as rio
import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely_geojson import dumps, Feature, FeatureCollection
from shapely_geojson import dump as featureDump
from matplotlib.colors import ListedColormap

import plotly.graph_objects as go

bString = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[8.2012939453125,55.32601943701404],[8.77532958984375,55.32601943701404],[8.77532958984375,55.658996099428364],[8.2012939453125,55.658996099428364],[8.2012939453125,55.32601943701404]]]}}]}'
user = "phun"
password = "cop38@sentinel"
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

area = json.loads(bString)
boundary = gpd.GeoDataFrame.from_features(area)

footprint = None
for i in boundary['geometry']:
    footprint = i

products = api.query(footprint,
                          date=('20210601', '20210930'),
                          platformname='Sentinel-2',
                          area_relation='Contains',
                          processinglevel='Level-2A',
                          cloudcoverpercentage=(0, 20))
gdf = api.to_geodataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

identifier = gdf_sorted.identifier[0]
bounds = gdf_sorted.boundary[0].bounds
minx = bounds[0]
maxy = bounds[3]


np.seterr(divide='ignore', invalid='ignore')

S_sentinel_bands = glob("Bands/*.jp2")

S_sentinel_bands.sort()

#image0 = cv2.imread('NIR_OLDDD.jp2')
#resized_nir = cv2.resize(image0, (5490, 5490))
#cv2.imwrite('Bands/NIR_OLDDD.jp2', resized_nir)

l = []

for i in S_sentinel_bands:
    with rio.open(i, 'r') as f:
        l.append(f.read(1))

arr_st = np.stack(l)

#ep.plot_bands(arr_st,
#              cmap = 'gist_earth',
#              figsize = (20, 12),
#              cols = 6,
#              cbar = False)
#plt.show()

NIR = arr_st[0]
SWIR1 = arr_st[1]

NNDMI = ((NIR - SWIR1)/(NIR + SWIR1))
img_blur = cv2.GaussianBlur(NNDMI,(7,7), sigmaX=0, sigmaY=0)
cv2.imwrite('disimg2.jp2', img_blur)
img_blur_img = cv2.imread('disimg2.jp2')

imgGry = cv2.cvtColor(img_blur_img, cv2.COLOR_BGR2GRAY)

ret, thrash = cv2.threshold(imgGry, 17, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#ep.plot_bands(thrash, cmap="RdYlGn", cols=1, vmin=-1, vmax=255, figsize=(10, 14))

ref_img = cv2.imread('Bands/NIR_B08_10m.jp2')

src = osr.SpatialReference()
src.SetWellKnownGeogCS("WGS84")
dataset = gdal.Open("T32UMG_20210716T103629_B03_20m.jp2")
GT = dataset.GetGeoTransform()
dataset2 = gdal.Open("T32UMG_20210716T103629_B02_10m.jp2")
GT2 = dataset2.GetGeoTransform()

present_img = cv2.drawContours(ref_img, contours, -1, (0,255,0), 3)

#plt.imshow(present_img)

#plt.show()
tmpvalyes = contours[1][0][0][0]
print(tmpvalyes)

pixelLatLongVal = 0.00018000018
feature_list = []

for i, contour in enumerate(contours):
    points = []
    for j, point in enumerate(contour):
        if i != 0 and len(contour) > 2 :
            pX = contours[i][j][0][0]
            pY = contours[i][j][0][1]

            latX = minx + (pX*pixelLatLongVal)
            x_geo = (GT[0] + (pX * GT[1]) + (pY * GT[2]))/100000
            y_geo = (GT[3] + (pX * GT[4]) + (pY * GT[5]))/100000
            lonY = maxy - (pY*pixelLatLongVal)
            print('x: ' + str(x_geo) + '\t y: ' + str(y_geo))
            points.append((x_geo, y_geo))
    feature_list.append(Polygon(points))

#p1 = Polygon([(1,20),(7,4),(4,3),(7,20)])
#p2 = Polygon([(11,10),(17,14),(14,13),(17,10)])
#print(p1.area)
#f1 = Feature(p1, {'index': 1})
#f2 = Feature(p2, {'index': 2})
#features = [f1, f2]
fcol = FeatureCollection(feature_list)
shapeString = dumps(fcol)
print(shapeString)

with open('shapers.json', 'w') as outfile:
    featureDump(fcol, outfile)

print("")
print(GT[0]/100000)
print(GT[3]/100000)


