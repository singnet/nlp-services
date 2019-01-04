FROM microsoft/cntk:latest

ARG git_owner
ARG git_repo
ARG git_branch

ENV SINGNET_REPOS=/opt/singnet
ENV GITHUB_REPO_NAME=${git_repo}
ENV SERVICES_FOLDER=${SINGNET_REPOS}/${GITHUB_REPO_NAME}
ENV SERVICE_NAME=cntk-language-understanding
ENV SNETD_HOST=54.203.198.53
ENV SNETD_PORT=7075
ENV SNETD_CONFIG=snetd.config.json

RUN mkdir -p ${SERVICES_FOLDER}

RUN apt-get update && \
    apt-get install -y apt-utils

RUN apt-get install -y \
    git \
    wget \
    nano

RUN cd ${SINGNET_REPOS} && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.4/snetd-0.1.4.tar.gz && \
    tar -xvf snetd-0.1.4.tar.gz && \
    mv snetd-0.1.4/snetd-linux-amd64 /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone -b ${git_branch} https://github.com/${git_owner}/${GITHUB_REPO_NAME}.git

RUN cd ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/nlp-services/${SERVICE_NAME} && \
    sh -c "echo '{ \"DAEMON_END_POINT\": \"http://${SNETD_HOST}:${SNETD_PORT}\", \
                   \"ETHEREUM_JSON_RPC_ENDPOINT\": \"https://kovan.infura.io\", \
                   \"IPFS_END_POINT\": \"http://ipfs.singularitynet.io:80\", \
                   \"REGISTRY_ADDRESS_KEY\": \"0xe331bf20044a5b24c1a744abc90c1fd711d2c08d\", \
                   \"PASSTHROUGH_ENABLED\": true, \
                   \"PASSTHROUGH_ENDPOINT\": \"http://localhost:7003\", \
                   \"ORGANIZATION_ID\": \"snet\", \
                   \"SERVICE_ID\": \"${SERVICE_NAME}\", \
                   \"LOG\": { \
                   \"LEVEL\": \"debug\" \
                   } \
                }'" > ${SNETD_CONFIG}

RUN cd ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/nlp-services/${SERVICE_NAME} && \
    /root/anaconda3/envs/cntk-py35/bin/python -m pip install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/nlp-services/${SERVICE_NAME}