FROM microsoft/cntk:latest

ARG GITHUB_ACCOUNT="singnet"
ARG GITHUB_BRANCH="master"
ARG GITHUB_REPO="nlp-services"
ARG SNETD_VERSION="v0.1.8"

ENV SERVICE_FOLDER="cntk-language-understanding"

RUN apt-get update && \
    apt-get install -y apt-utils

RUN apt-get install -y \
    git \
    wget \
    nano

ADD https://github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}/raw/${GITHUB_BRANCH}/${SERVICE_FOLDER}/requirements.txt /tmp/service_requirements.txt
RUN /root/anaconda3/envs/cntk-py35/bin/python -m pip install -r /tmp/service_requirements.txt

ADD https://api.github.com/repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/compare/${GITHUB_BRANCH}...HEAD /dev/null
RUN git clone -b ${GITHUB_BRANCH} https://github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}.git && \
    mv ${GITHUB_REPO}/${SERVICE_FOLDER}/ /${SERVICE_FOLDER} && \
    rm -rf ${GITHUB_REPO}

RUN cd /${SERVICE_FOLDER} && \
    bash buildproto.sh

ADD https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz /tmp/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz
RUN cd /tmp && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd && \
    rm -rf snet-daemon-${SNETD_VERSION}-linux-amd64*

WORKDIR /${SERVICE_FOLDER}