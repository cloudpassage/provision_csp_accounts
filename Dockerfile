FROM ubuntu:16.04 as tester
MAINTAINER awilson@cloudpassage.com

RUN apt-get update && \
    apt-get install -y \
        python2.7 \
        python-pip

RUN mkdir /app/

COPY . /app/

WORKDIR /app/

RUN pip install -r requirements-test.txt

RUN python2.7 -m py.test \
    --cov=provisioner  \
    --cov-report term-missing \
    /app/test
