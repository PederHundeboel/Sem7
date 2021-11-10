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
from collections import defaultdict
import unittest
from src import secrets
from src.downloader import Downloader
import happybase

class MockConnection(object):
    ''' singleton object, so that multiple HBaseTables can collaborate '''

    _instance = None
    tables = dict()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MockConnection, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def is_table_enabled(self, name):
        return True

    def table(self, name):
        table = self.tables.get(name)
        if not table:
            table = MockTable(name)
            self.tables[name] = table
        return table

    def flush(self):
        self.tables = dict()

class MockTable(object):

    def __init__(self, table_name):
        self.table_name = table_name
        self.data = defaultdict(dict)

    def put(self, row, data):
        self.data[row].update(data)

    def row(self, row, columns=None):
        return self.data[row]

    def scan(self, **options):
        ''' does not respect any options like start/stop row '''
        return self.data.items()

class HBaseTestCase(unittest.TestCase):
    ''' mock out calls to hbase
    if you over-ride setUp(), make sure to call super '''

    def setUp(self):
        happybase._Connection = happybase.Connection
        happybase.Connection = MockConnection
        MockConnection().flush()

    def tearDown(self):
        happybase.Connection = happybase._Connection


class HappybaseMockTests(HBaseTestCase):
    def setUp(self):
        connection = happybase.Connection()
        self.table = connection.table('sentinel-raw')
        super(HappybaseMockTests, self).setUp()


hmbt = HappybaseMockTests()
hmbt.setUp()
rawtable = hmbt.table

d = Downloader(secrets.USER, secrets.PASSWORD, None, rawtable)
m = d.query('{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[8.2012939453125,55.32601943701404],[8.77532958984375,55.32601943701404],[8.77532958984375,55.658996099428364],[8.2012939453125,55.658996099428364],[8.2012939453125,55.32601943701404]]]}}]}')
print('IDENTIFIER WAS: ' + m)



