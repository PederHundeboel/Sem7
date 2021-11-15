docker build . -t producer:latest 
docker run --network hadoop producer

:: stop/remove all:             docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker volume rm kafka_volume
:: start hdfs-connect-sink:     curl -s -X POST -H 'Content-Type: application/json' --data @hdfs-sink.json http://localhost:8083/connectors
:: start hsbase sink:           curl -s -X POST -H 'Content-Type: application/json' --data @hbase-sink.json http://localhost:8083/connectors

