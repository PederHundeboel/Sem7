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
    row = table.row('adf7c8d7c7ea45a5aa6be354a8f13d61')
    #print(row)

    coordinates = json.dumps(row[b'products:features'])
    print(coordinates)

    id = row[b'products:id'].decode("utf-8")
    print(id)
    #print(row[b'products:shape'])  # prints 'value1'
    #for key, data in table.scan():
    #    print(key, data)


    # test
    #df = pdh.read_hbase(connection, 'products-avro', '', cf=b'dimensions:dimensions1')
    #print(df)
finally:
    if connection:
        connection.close()