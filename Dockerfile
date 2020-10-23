FROM python:3.8.6-slim-buster

RUN apt-get -y update && \
    apt-get -y install git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt