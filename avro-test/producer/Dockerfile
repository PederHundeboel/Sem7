#FROM python:3.6

#WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#CMD [ "python", "./avro-producer.py" ]

# cron stuff 
#FROM python:3.9.0b4-alpine3.12
#COPY avro-producer.py /bin/avro-producer.py
#COPY requirements.txt ./
#COPY root /var/spool/cron/crontabs/root
#RUN pip install --no-cache-dir -r requirements.txt
#RUN chmod +x /bin/avro-producer.py
#CMD crond -l 2 -f
FROM python:3.7
RUN apt-get update && apt-get -y install cron vim
WORKDIR /usr/src/app

COPY avro-producer.py ./avro-producer.py
COPY features.json ./features.json
COPY schema ./schema

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
#CMD ["cron", "-f"]

CMD [ "python", "./avro-producer.py" ]
