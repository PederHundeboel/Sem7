import glob
import os.path

import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt
import tempfile as tmp
import shutil
from kafka import KafkaProducer
from kafka import KafkaConsumer
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from sentinelsat.sentinel import SentinelAPI


#image = cv2.imread('g2.jp2')
#cv2.imwrite('g2.png', image)

def queryBoundary(boundaryString):
    boundary = gpd.read_file(boundaryString)

    user = "phun"
    password = "cop38@sentinel"

    footprint = None
    for i in boundary['geometry']:
        footprint = i

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    products = api.query(footprint,
                         date=('20210601', '20210930'),
                         platformname='Sentinel-2',
                         area_relation='Contains',
                         processinglevel='Level-2A',
                         cloudcoverpercentage=(0, 20))

    gdf = api.to_geodataframe(products)
    gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    print(boundaryString)
    api.download(gdf_sorted.uuid[0])


def downloadFromUUID(idddddddddeeesnuts):
    dirpath = tmp.mkdtemp()
    bandpath = tmp.mkdtemp()
    print(os.path.abspath(dirpath))
    shutil.unpack_archive('S2A_MSIL2A_20210923T170031_N0301_R069_T14RPP_20210923T214645.zip', dirpath)
    print('SHIT : ' + str(glob.glob(dirpath +'/*/GRANULE/*/IMG_DATA/R10m/*B08_10m.jp2')))
    shutil.move(glob.glob(dirpath +'/*/GRANULE/*/IMG_DATA/R10m/*B08_10m.jp2')[0], bandpath+'/NIR.jp2')
    shutil.move(glob.glob(dirpath +'/*/GRANULE/*/IMG_DATA/R20m/*B11_20m.jp2')[0], bandpath + '/SWIR.jp2')
    print('SWIR exists' + str(os.path.exists(bandpath+'/SWIR.jp2')))
    shutil.rmtree(bandpath)
    shutil.rmtree(dirpath)


def visualize(boundaryString):
    boundary = gpd.read_file(boundaryString)

    bands = 'Bands'
    blue = rasterio.open(r'2blue_B02_10m.jp2')
    green = rasterio.open(r'2green_B03_10m.jp2')
    red = rasterio.open(r'2red_B04_10m.jp2')
    with rasterio.open('image_name.tiff', 'w', driver='Gtiff', width=blue.width, height=blue.height, count=3,
                       crs=blue.crs, transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1), 3)
        rgb.write(green.read(1), 2)
        rgb.write(red.read(1), 1)
        rgb.close()

    check = rasterio.open('image_name.tiff')
    check.crs

    bound_crs = boundary.to_crs({'init': check.crs})
    with rasterio.open("image_name.tiff") as src:
        out_image, out_transform = mask(src,
                                        bound_crs.geometry, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

    with rasterio.open("masked_image.tif", "w", **out_meta) as final:
        final.write(out_image)

    src = rasterio.open(r'masked_image.tif')
    plt.figure(figsize=(6, 6))
    plt.title('Final Image')
    plot.show(src, adjust='linear')


#locationToPng('Resources/g2.geojson')
downloadFromUUID(1)