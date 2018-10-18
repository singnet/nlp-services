FROM ubuntu:18.04
WORKDIR /
ENV GOPATH=/singnet
ENV SINGNET_REPOS=${GOPATH}/src/github.com/singnet
ENV PATH=${GOPATH}/bin:${PATH}
ENV PATH=${PATH}:/singnet/src/github.com/singnet/snet-daemon/build

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    nano \
    git \
    wget \
    curl \
    apt-utils \
    sudo \
    libudev-dev \
    libusb-1.0-0-dev

RUN apt-get install -y golang go-dep golang-goprotobuf-dev golint
RUN apt-get install -y nodejs npm
RUN apt-get install -y python3 python3-pip

RUN cd / && \
    mkdir -p singnet/src/github.com/singnet && \
    mkdir -p ${GOPATH}/ipfs && \
    cd $GOPATH && \
    mkdir log && \
    cd $SINGNET_REPOS && \
    git clone https://github.com/singnet/platform-contracts && \
    cd platform-contracts && \
    npm install && \
    npm install ganache-cli && \
    ./node_modules/.bin/truffle compile
RUN cd $SINGNET_REPOS && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.0/snetd-0.1.0.tar.gz && \
    tar -xvf snetd-0.1.0.tar.gz && \
    mv snetd-linux-amd64 snetd
RUN cd $SINGNET_REPOS && \
    git clone https://github.com/singnet/nlp-services.git && \
    cd $SINGNET_REPOS/nlp-services/named-entity-recognition && \
    cp $SINGNET_REPOS/snet-daemon/snetd-linux-amd64 ./snetd && \
    ln -s $SINGNET_REPOS/snet-daemon/build/snetd-linux-amd64 ./snetd && \
    pip3 install -r requirements.txt && \
    python3 -c "import nltk; nltk.download('punkt')" && \
    bash buildproto.sh

WORKDIR  $SINGNET_REPOS/nlp-services/named-entity-recognition
EXPOSE 7010-7011
CMD ["python3", "run_service.py", "--daemon-conf", "config/"]
