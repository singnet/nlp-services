FROM nvidia/cuda:9.1-cudnn7-devel-ubuntu16.04
ENV DEBIAN_FRONTEND noninteractive
ARG GITHUB_ACCOUNT="singnet"
ARG SNETD_VERSION="v0.1.8"
RUN apt-get update && apt-get install -y locales software-properties-common git
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
      apt-get update && \
      apt-get upgrade -y && \
      apt-get install -y python3.6 python3.6-dev build-essential cmake libgtk2.0-dev python3.6-tk && \
      curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

ADD https://raw.githubusercontent.com/OpenNMT/OpenNMT-py/master/requirements.txt /opennmt_requirements.txt
RUN apt-get install -y git default-jre && pip3.6 install -r opennmt_requirements.txt && pip3.6 install numpy -I

ADD https://github.com/$GITHUB_ACCOUNT/nlp-services/raw/master/text-summarization/requirements.txt /service_requirements.txt
RUN pip3.6 install -r service_requirements.txt

ADD https://api.github.com/repos/${GITHUB_ACCOUNT}/nlp-services/compare/master...HEAD /dev/null
RUN git clone https://github.com/${GITHUB_ACCOUNT}/nlp-services.git && \
    cd nlp-services/text-summarization && \
    python3.6 ../fetch_models.py && \
    git submodule update --init -- opennmt-py && \
    cd .. && mv text-summarization/ /text-summarization && \
    rm -rf /nlp-services

ADD https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz /snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz
RUN tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd && \
    rm -rf /snet-daemon-${SNETD_VERSION}-linux-amd64

WORKDIR /text-summarization
RUN bash buildproto.sh