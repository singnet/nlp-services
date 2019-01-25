#Sentiment Analysis.
FROM ubuntu:18.04
WORKDIR /
ENV GOPATH=/singnet
ENV SINGNET_REPOS=${GOPATH}/src/github.com/singnet
ENV PATH=${GOPATH}/bin:${PATH}
ENV PATH=${PATH}:/singnet/src/github.com/singnet/snet-daemon

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    nano \
    git \
    wget \
    curl \
    apt-utils \
    net-tools \
    sudo \
    libudev-dev \
    libusb-1.0-0-dev

RUN apt-get install -y python3 python3-pip

RUN cd / && \
    mkdir -p singnet/src/github.com/singnet && \
    mkdir -p ${GOPATH}/ipfs && \
    cd $SINGNET_REPOS && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.6/snet-daemon-v0.1.6-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-v0.1.6-linux-amd64.tar.gz && \
    mv snet-daemon-v0.1.6-linux-amd64/snetd ./snetd

RUN cd $SINGNET_REPOS && \
    git clone https://github.com/glautervl/nlp-services.git && \
    cd $SINGNET_REPOS/nlp-services/sentiment-analysis && \
    pip3 install -r requirements.txt && \
    python3 -c "import nltk; nltk.download('punkt')" && \
    python3 -c "import nltk; nltk.download('vader_lexicon')" && \
    bash buildproto.sh

WORKDIR  $SINGNET_REPOS/nlp-services/sentiment-analysis
EXPOSE 7010-7011
CMD ["python3", "run_service.py"]
