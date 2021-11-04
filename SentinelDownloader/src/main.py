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

from src import secrets
from src.downloader import Downloader

d = Downloader(secrets.USER, secrets.PASSWORD, None)
d.query('{   "type": "FeatureCollection",   "features": [     {       "type": "Feature",       "properties": {},       "geometry": {         "type": "Polygon",         "coordinates": [           [             [               8.2012939453125,               55.32601943701404             ],             [               8.77532958984375,               55.32601943701404             ],             [               8.77532958984375,               55.658996099428364             ],             [               8.2012939453125,               55.658996099428364             ],             [               8.2012939453125,               55.32601943701404             ]           ]         ]       }     }   ] }')
