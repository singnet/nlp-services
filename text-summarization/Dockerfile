FROM nvidia/cuda:9.1-cudnn7-devel-ubuntu16.04
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
      apt-get update && \
      apt-get upgrade -y && \
      apt-get install -y python3.6 python3.6-dev build-essential cmake libgtk2.0-dev python3.6-tk && \
      curl https://bootstrap.pypa.io/get-pip.py | python3.6

ADD opennmt-py/requirements.txt /opennmt_requirements.txt
RUN apt-get install -y git default-jre && pip3.6 install -r opennmt_requirements.txt && pip3.6 install numpy -I

ADD requirements.txt /service_requirements.txt
RUN pip3.6 install -r service_requirements.txt

ADD . /text-summarization
WORKDIR /text-summarization

CMD ["python3.6", "run_service.py"]