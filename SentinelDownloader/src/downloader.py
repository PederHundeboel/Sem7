import glob
import os.path
import json
import shutil
import geopandas as gpd
import happybase
import re
from sentinelsat.sentinel import SentinelAPI
from kafka import KafkaProducer
import tempfile as tmp


class Downloader:
    def __init__(self, user, pw, connection: happybase.Connection):
        self.api = SentinelAPI(user, pw, 'https://scihub.copernicus.eu/dhus')
        #self.dbconn = connection
        #self.raw_table = self.dbconn.table('sentinel-raw')
        #self.processed_table = self.dbconn.table('processed')
        self.dirpath = None
        self.bandpath = None

    def query(self, boundaryString):

        area = json.loads(boundaryString)
        boundary = gpd.GeoDataFrame.from_features(boundaryString)

        footprint = None
        for i in boundary['geometry']:
            footprint = i

        products = self.api.query(footprint,
                                  date=('20210601', '20210930'),
                                  platformname='Sentinel-2',
                                  area_relation='Contains',
                                  processinglevel='Level-2A',
                                  cloudcoverpercentage=(0, 20))
        gdf = self.api.to_geodataframe(products)
        gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

        identifier = gdf_sorted.identifier[0]

        if False: #self.__check_key(identifier, self.processed_table):
            print('Data for identifier ' + identifier + 'was already processed')
        elif False: #self.__check_key(identifier, self.raw_table):
            print()
        else:
            try:
                self.download()
            except:
                print('Download failed for ' + identifier)
        return identifier

    def download(self, uuid):
        self.api.download(uuid)

    def unpack(self, identifier):
        self.dirpath = tmp.mkdtemp()
        self.bandpath = tmp.mkdtemp()
        sentinelFileName = glob.glob(os.getcwd() + '/S2*')[0]
        shutil.unpack_archive(sentinelFileName, self.dirpath)
        print('unpacked glob.glob' + (os.getcwd() + '/S2*')[0] + 'to ' + self.dirpath)
        shutil.move(glob.glob(self.dirpath + '/*/GRANULE/*/IMG_DATA/R10m/*B08_10m.jp2')[0], self.dirpath + '/NIR.jp2')
        shutil.move(glob.glob(self.dirpath + '/*/GRANULE/*/IMG_DATA/R20m/*B11_20m.jp2')[0], self.dirpath + '/SWIR.jp2')
        shutil.move(self.bandpath, self.dirpath + '/')
        self.__save_in_hbase(identifier)

    def __save_in_hbase(self, identifier):
        #jp2's probably can not be saved directly to hbase
        nir = open(self.dirpath + '/NIR.jp2')
        nirData = nir.read()
        swir = open(self.dirpath + '/SWIR.jp2')
        swirData = swir.read()
        #self.raw_table.put(identifier, {'cf:nir_band': nirData, 'cf:swir_band': swirData})
        self.__cleanup()

    def __check_key(self, identifier, table: happybase.Table):
        scan = table.scan(
            row_start=identifier,
            filter='KeyOnlyFilter() AND FirstKeyOnlyFilter()',
            limit=1)
        if next(scan, None) is not None:
            return True
        else:
            return False

    def __cleanup(self):
        shutil.rmtree(self.bandpath)
        shutil.rmtree(self.dirpath)


