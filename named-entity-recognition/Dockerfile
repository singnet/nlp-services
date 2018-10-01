FROM golang:latest
WORKDIR /
RUN apt-get update && apt-get install -y \
    nano \
    wget \
    build-essential \
    checkinstall \
    zlib1g-dev \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libusb-1.0-0-dev \
    libudev1 \
    libudev-dev \
    protobuf-compiler \
    libprotobuf-dev && \
    rm -rf /var/lib/apt/lists/*
RUN go get -v -u github.com/golang/dep/cmd/dep && \
    go get -v -u github.com/golang/protobuf/protoc-gen-go && \
    go get -v -u github.com/golang/protobuf/protoc-gen-go && \
    go get -v -u github.com/golang/lint/golint
RUN curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh && \
    chmod 755 nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    rm -f nodesource_setup.sh
RUN cd /go/src && \
    wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz && \
    tar xvf Python-3.6.5.tar.xz && \
    cd /go/src/Python-3.6.5 && \
    ./configure && \
    make -j8 && \
    make altinstall && \
    cd /go/src && \
    rm -rf Python-3.6.5 && \
    rm -f Python-3.6.5.tar.xz && \
    pip3.6 install --upgrade pip
RUN mkdir -p /go/src/github.com/singnet && \
    cd /go/src/github.com/singnet && \
    git clone https://github.com/singnet/snet-daemon.git && \
    cd /go/src/github.com/singnet/snet-daemon && \
    ./scripts/install && \
    ./scripts/build linux amd64 && \
    cp ./build/snetd-linux-amd64 /go/bin/snetd && \
    pip3.6 install snet_cli && \
    cd /go/src && \
    git clone https://github.com/singnet/nlp-services.git && \
    cd /go/src/nlp-services/named-entity-recognition && \
    pip3.6 install -r requirements.txt && \
    RUN python3.6 -c "import nltk; nltk.download('punkt')" && \
    bash buildproto.sh
WORKDIR /go/src/nlp-services/named-entity-recognition
EXPOSE 7012-7013
CMD ["python3.6", "run_service.py", "--daemon-conf", "config/"]