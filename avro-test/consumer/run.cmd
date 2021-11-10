docker build . -t producer:latest 
docker run --rm --network docker-network -it consumer /bin/bash