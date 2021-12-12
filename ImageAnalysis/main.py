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
from shapely_geojson import dumps, FeatureCollection
from shapely_geojson import dump as featureDump
from matplotlib.colors import ListedColormap
from pyproj import Proj, transform
import pyproj
import jp2helper
import utm

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

NIR = arr_st[0]
SWIR1 = arr_st[1]

NNDMI = ((NIR - SWIR1)/(NIR + SWIR1))
img_blur = cv2.GaussianBlur(NNDMI,(7,7), sigmaX=0, sigmaY=0)
cv2.imwrite('disimg2.jp2', img_blur)
img_blur_img = cv2.imread('disimg2.jp2')

imgGry = cv2.cvtColor(img_blur_img, cv2.COLOR_BGR2GRAY)

ret, thrash = cv2.threshold(imgGry, 17, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

ref_img = cv2.imread('Bands/NIR_B08_10m.jp2')

dataset = gdal.Open("T32UMG_20210716T103629_B03_20m.jp2")
imageGeoTrans = dataset.GetGeoTransform()


utm_zone_info = utm.from_latlon(maxy, minx)

present_img = cv2.drawContours(ref_img, contours, -1, (0,255,0), 3)

plt.imshow(present_img)

plt.show()

feature_list = []


for i, contour in enumerate(contours):
    points = []
    for j, point in enumerate(contour):
        if i != 0 and len(contour) > 2 :
            #Pixel offsets
            pX = contours[i][j][0][0]
            pY = contours[i][j][0][1]
            #Calculate utm position based on pixel offsets
            x_utm = (imageGeoTrans[0] + ((pX + 0.5) * imageGeoTrans[1]) + (pY * imageGeoTrans[2]))
            y_utm = (imageGeoTrans[3] + ((pX + 0.5) * imageGeoTrans[4]) + (pY * imageGeoTrans[5]))
            #Project calculated utm position to LatLon
            projectedLatLon = utm.to_latlon(x_utm, y_utm, utm_zone_info[2], zone_letter=utm_zone_info[3])
            points.append((projectedLatLon[1], projectedLatLon[0]))
    feature_list.append(Polygon(points))

fcol = FeatureCollection(feature_list)

with open('shapers.json', 'w') as outfile:
    featureDump(fcol, outfile)



