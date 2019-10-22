#Sentiment Analysis.
FROM ubuntu:18.04

ARG GITHUB_ACCOUNT="singnet"
ARG GITHUB_BRANCH="master"
ARG GITHUB_REPO="nlp-services"
ARG SNETD_VERSION="v2.0.2"

ENV SERVICE_FOLDER="sentiment-analysis"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    nano \
    git \
    wget \
    curl \
    apt-utils \
    net-tools \
    lsof \
    sudo \
    libudev-dev \
    libusb-1.0-0-dev

RUN apt-get install -y python3 python3-pip

ADD https://github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}/raw/${GITHUB_BRANCH}/${SERVICE_FOLDER}/requirements.txt /tmp/service_requirements.txt
RUN pip3 install -r /tmp/service_requirements.txt

ADD https://api.github.com/repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/compare/${GITHUB_BRANCH}...HEAD /dev/null
RUN git clone -b ${GITHUB_BRANCH} https://github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}.git && \
    cd ${GITHUB_REPO}/${SERVICE_FOLDER} && \
    python3 ../fetch_models.py && \
    cd .. && mv ${SERVICE_FOLDER}/ /${SERVICE_FOLDER} && \
    rm -rf /${GITHUB_REPO}

RUN cd /${SERVICE_FOLDER} && \
    python3 -c "import nltk; nltk.download('punkt')" && \
    python3 -c "import nltk; nltk.download('vader_lexicon')" && \
    bash buildproto.sh

ADD https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz /tmp/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz
RUN cd /tmp && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd && \
    rm -rf snet-daemon-${SNETD_VERSION}-linux-amd64*

WORKDIR /${SERVICE_FOLDER}