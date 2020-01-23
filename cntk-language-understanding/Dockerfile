FROM microsoft/cntk:2.5-gpu-python3.5-cuda9.0-cudnn7.0

ARG GITHUB_ACCOUNT="singnet"
ARG GITHUB_REPO="nlp-services"
ARG GITHUB_BRANCH="master"

ENV SINGNET_DIR=/opt/singnet
ENV SERVICE_NAME=cntk-language-understanding

RUN mkdir -p ${SINGNET_DIR}

RUN apt-get update && \
    apt-get install -y \
    git \
    wget \
    curl \
    nano

# Install snet daemon
RUN SNETD_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'` && \
    cd /tmp && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_DIR} && \
    git clone -b ${GITHUB_BRANCH} https://github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}.git

RUN cd ${SINGNET_DIR}/${GITHUB_REPO}/${SERVICE_NAME} && \
    /root/anaconda3/envs/cntk-py35/bin/python -m pip install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_DIR}/${GITHUB_REPO}/${SERVICE_NAME}
