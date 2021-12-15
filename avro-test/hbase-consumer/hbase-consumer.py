import happybase
import numpy as np
import pandas as pd
#import pdhbase as pdh
import pdhhbase as pdh
import json 

connection = None
try:
    connection = happybase.Connection('hbase')
    connection.open()

    #print(connection.tables())
    table = connection.table('products-avro')
    row = table.row('1e47823319d442ecb3182f7fb9366bd0')
    #print(row)

    coordinates = row[b'products:geojson'].decode("utf-8")
    #print(coordinates)

    with open('test.json', 'w') as f:
        f.write(coordinates)

    #id = row[b'products:id'].decode("utf-8")
    #print(id)

finally:
    if connection:
        connection.close()