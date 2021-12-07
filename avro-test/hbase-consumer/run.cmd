docker build . -t consumer:latest 
docker run --network hadoop -it consumer /bin/bash