import json
from glob import glob
from sentinelsat.sentinel import SentinelAPI
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import geopandas as gpd
import rasterio as rio
import cv2
import matplotlib.pyplot as plt
import numpy as np
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
contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

ep.plot_bands(thrash, cmap="RdYlGn", cols=1, vmin=-1, vmax=255, figsize=(10, 14))

ref_img = cv2.imread('Bands/NIR_B08_10m.jp2')

present_img = cv2.drawContours(ref_img, contours, -1, (0,255,0), 3)

plt.imshow(present_img)

plt.show()
