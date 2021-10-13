import folium
import geopandas as gpd
import rasterio as rasterio
from sentinelsat.sentinel import SentinelAPI
import rasterio
import cv2
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from osgeo import gdal

#image0 = cv2.imread('NIR.jp2')

#cv2.imwrite('nir.png', image0)

def locationToPng(boundaryString):
    boundary = gpd.read_file(boundaryString)

    user = "phun"
    password = "cop38@sentinel"

    footprint = None
    for i in boundary['geometry']:
        footprint = i

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    products = api.query(footprint,
                         date=('20210901', '20210930'),
                         platformname='Sentinel-2',
                         processinglevel='Level-2A',
                         cloudcoverpercentage=(0, 20))

    gdf = api.to_geodataframe(products)
    gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    print(boundaryString)
    api.download(gdf_sorted.uuid[0])


locationToPng('Resources/g1.geojson')
#locationToPng('Resources/g2.geojson')
#locationToPng('Resources/g3.geojson')
#locationToPng('Resources/g4.geojson')
#locationToPng('Resources/g5.geojson')
#locationToPng('Resources/g6.geojson')

