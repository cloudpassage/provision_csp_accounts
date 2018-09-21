FROM ubuntu:16.04 as tester
MAINTAINER toolbox@cloudpassage.com

ARG CC_TEST_REPORTER_ID

RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        python2.7 \
        python-pip

RUN mkdir /app/

COPY . /app/

WORKDIR /app/

RUN pip install -r requirements-test.txt

# Codeclimate setup
RUN curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
RUN chmod +x ./cc-test-reporter
RUN ./cc-test-reporter before-build

# Run tests
RUN python2.7 -m py.test \
    --cov=provisioner  \
    --cov-report term-missing \
    --cov-report xml \
    /app/test

# Send coverage results to Codeclimate
RUN ./cc-test-reporter after-build

##################################
FROM ubuntu:16.04
