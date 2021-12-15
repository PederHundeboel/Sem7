docker build . -t consumer:latest 
docker run --network hadoop -it consumer /bin/bash

:: get id of row from hbase to collect geojson:            count 'products-avro', INTERVAL=> 1
:: copy test.json of geojson to host for viewing:            docker cp 0b605b23be3d:/usr/src/app/test.json /mnt/c/Users/vlocn/OneDrive/Dokumenter/Skole/git/Sem7