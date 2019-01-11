FROM nvidia/cuda:8.0-devel-ubuntu16.04 as torch_builder

RUN apt update && \
    apt install -y \
        autoconf \
        automake \
        build-essential \
        cmake \
        curl \
        g++ \
        gcc \
        git \
        libprotobuf-dev \
        libprotobuf9v5 \
        libreadline-dev \
        libtool \
        libzmq-dev \
        pkg-config \
        protobuf-compiler \
        unzip \
        nano \
        wget

# Fetch Intel MKL.
RUN mkdir /root/mkl && \
    wget https://anaconda.org/intel/mkl/2018.0.1/download/linux-64/mkl-2018.0.1-intel_4.tar.bz2 && \
    tar -xf mkl-2018.0.1-intel_4.tar.bz2 -C /root/mkl && \
    rm mkl-2018.0.1-intel_4.tar.bz2
ENV MKL_ROOT=/root/mkl
RUN rm -f $MKL_ROOT/lib/*vml* \
          $MKL_ROOT/lib/*ilp64* \
          $MKL_ROOT/lib/*blacs* \
          $MKL_ROOT/lib/*scalapack* \
          $MKL_ROOT/lib/*cdft* \
          $MKL_ROOT/lib/libmkl_tbb_thread.so \
          $MKL_ROOT/lib/libmkl_ao_worker.so

# Compile Torch and OpenNMT dependencies.
ARG CUDA_ARCH
ENV CUDA_ARCH=${CUDA_ARCH:-Common}
RUN git clone https://github.com/torch/distro.git /root/torch-distro --recursive && \
    cd /root/torch-distro && \
    mkdir /root/torch && \
    CMAKE_LIBRARY_PATH=$CMAKE_LIBRARY_PATH:$MKL_ROOT/lib \
    TORCH_CUDA_ARCH_LIST=${CUDA_ARCH} TORCH_NVCC_FLAGS="-Xfatbin -compress-all" \
    PREFIX=/root/torch ./install.sh
RUN cp -r $MKL_ROOT/lib/* /root/torch/lib
RUN /root/torch/bin/luarocks install tds && \
    /root/torch/bin/luarocks install dkjson && \
    /root/torch/bin/luarocks install restserver-xavante && \
    /root/torch/bin/luarocks install yaml && \
    /root/torch/bin/luarocks install bit32 && \
    /root/torch/bin/luarocks install luacheck && \
    /root/torch/bin/luarocks install luacov && \
    /root/torch/bin/luarocks install lua-zmq \
        ZEROMQ_LIBDIR=/usr/lib/x86_64-linux-gnu/ ZEROMQ_INCDIR=/usr/include

# Install lua-sentencepiece
RUN git clone https://github.com/google/sentencepiece.git /root/sentencepiece-git && \
    cd /root/sentencepiece-git && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/root/sentencepiece .. && \
    make -j $(nproc) && \
    make install && \
    rm -r /root/sentencepiece-git

RUN git clone https://github.com/OpenNMT/lua-sentencepiece.git /root/lua-sentencepiece && \
    cd /root/lua-sentencepiece && \
    CMAKE_LIBRARY_PATH=/root/sentencepiece/lib CMAKE_INCLUDE_PATH=/root/sentencepiece/include \
    /root/torch/bin/luarocks make lua-sentencepiece-scm-1.rockspec \
        LIBSENTENCEPIECE_DIR=/root/sentencepiece && \
    cd /root && \
    rm -r /root/lua-sentencepiece

FROM nvidia/cuda:8.0-runtime-ubuntu16.04
MAINTAINER OpenNMT <http://opennmt.net/>

ARG git_owner
ARG git_repo
ARG git_branch

ENV SINGNET_REPOS=/opt/singnet
ENV GITHUB_REPO_NAME=${git_repo}
ENV SERVICES_FOLDER=${SINGNET_REPOS}/${GITHUB_REPO_NAME}
ENV SERVICE_NAME=opennmt-romance-translator
ENV SNETD_HOST=54.203.198.53
ENV SNETD_PORT=7076
ENV SNETD_CONFIG=snetd.config.json

RUN mkdir -p ${SERVICES_FOLDER}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgomp1 \
        libprotobuf9v5 \
        libzmq1 \
        nano \
        wget \
        git \
        python3-pip \
        python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV TORCH_DIR=/root/torch
ENV SENTENCEPIECE_DIR=/root/sentencepiece

COPY --from=torch_builder /root/torch ${TORCH_DIR}
COPY --from=torch_builder /root/sentencepiece ${SENTENCEPIECE_DIR}

ENV LUA_PATH="${TORCH_DIR}/share/lua/5.1/?.lua;${TORCH_DIR}/share/lua/5.1/?/init.lua;./?.lua"
ENV LUA_CPATH="${TORCH_DIR}/lib/lua/5.1/?.so;./?.so;${TORCH_DIR}/lib/?.so"
ENV PATH=${TORCH_DIR}/bin:${PATH}
ENV LD_LIBRARY_PATH=${TORCH_DIR}/lib:${LD_LIBRARY_PATH}
ENV THC_CACHING_ALLOCATOR=0

ENV ONMT_DIR=/root/opennmt
COPY . $ONMT_DIR

RUN cd ${SINGNET_REPOS} && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.4/snetd-0.1.4.tar.gz && \
    tar -xvf snetd-0.1.4.tar.gz && \
    mv snetd-0.1.4/snetd-linux-amd64 /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone -b ${git_branch} https://github.com/${git_owner}/${GITHUB_REPO_NAME}.git

RUN cd ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/${SERVICE_NAME} && \
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

RUN cd ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/${SERVICE_NAME} && \
    cd utils/ && \
    ./prepare_data.sh ./data

RUN cd ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/${SERVICE_NAME} && \
    pip3 install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/${GITHUB_REPO_NAME}/${SERVICE_NAME}