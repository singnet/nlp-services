FROM nvidia/cuda:9.1-cudnn7-devel-ubuntu16.04
ENV DEBIAN_FRONTEND noninteractive 
RUN apt-get update && apt-get install -y locales software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
      apt-get update && \
      apt-get upgrade -y && \
      apt-get install -y python3.6 python3.6-dev build-essential cmake libgtk2.0-dev python3.6-tk && \
      curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

ADD opennmt-py/requirements.txt /opennmt_requirements.txt
RUN apt-get install -y git default-jre && pip3.6 install -r opennmt_requirements.txt && pip3.6 install numpy -I

ADD requirements.txt /service_requirements.txt
RUN pip3.6 install -r service_requirements.txt

# Install snet daemon
RUN curl -OL https://github.com/singnet/snet-daemon/releases/download/v0.1.0/snetd-0.1.0.tar.gz && \
      tar xzvf snetd-0.1.0.tar.gz && \
      cp snetd-linux-amd64 /usr/local/bin/snetd

ADD . /translation
WORKDIR /translation

CMD ["python3.6", "run_service.py"]