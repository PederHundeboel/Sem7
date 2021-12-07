import happybase
import numpy as np
import pandas as pd
#import pdhbase as pdh
import pdhhbase as pdh
connection = None
try:
    connection = happybase.Connection('hbase')
    connection.open()

    #print(connection.tables())
    table = connection.table('products-avro')
    row = table.row('c1c8736ada6a457abd4af68ec70a773a')
    print(row[b'dimensions:dimensions1'])  # prints 'value1'
    print(row)   # prints the value of cf1:col1
    #for key, data in table.scan():
    #    print(key, data)


    # test
    df = pdh.read_hbase(connection, 'products-avro', '', cf=b'dimensions:dimensions1')
    print(df)
finally:
    if connection:
        connection.close()