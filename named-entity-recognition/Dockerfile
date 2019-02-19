FROM ubuntu:18.04
ARG GITHUB_ACCOUNT=singnet

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

RUN apt-get install -y default-jre
RUN apt-get install -y python3 python3-pip

ADD https://github.com/${GITHUB_ACCOUNT}/nlp-services/raw/master/named-entity-recognition/requirements.txt /service_requirements.txt
RUN pip3 install -r service_requirements.txt

ADD https://api.github.com/repos/${GITHUB_ACCOUNT}/nlp-services/compare/master...HEAD /dev/null
RUN git clone https://github.com/${GITHUB_ACCOUNT}/nlp-services.git && \
    cd nlp-services/named-entity-recognition && \
    python3 ../fetch_models.py && \
    cd .. && mv named-entity-recognition/ /named-entity-recognition && \
    rm -rf /nlp-services

RUN cd /named-entity-recognition && \
    python3 -c "import nltk; nltk.download('punkt')" && \
    python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')" && \
    ls -la && \
    bash buildproto.sh

ADD https://github.com/singnet/snet-daemon/releases/download/v0.1.6/snet-daemon-v0.1.6-linux-amd64.tar.gz /snet-daemon-v0.1.6-linux-amd64.tar.gz
RUN tar -xvf snet-daemon-v0.1.6-linux-amd64.tar.gz && \
    mv snet-daemon-v0.1.6-linux-amd64/snetd /usr/bin/snetd && \
    rm -rf /snet-daemon-v0.1.6-linux-amd64

WORKDIR /named-entity-recognition
EXPOSE 7012-7013
CMD ["python3", "run_service.py"]
