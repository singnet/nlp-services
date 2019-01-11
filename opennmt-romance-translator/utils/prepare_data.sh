#!/usr/bin/env bash
if [ -z "$1" ]
  then
    echo "Invalid arguments: ./prepare_data.sh DATA_FOLDER"
    exit 1
fi

data="$1"
if [ ! -d "$data" ]
then
    mkdir $data
    cd $data

    echo "Downloading models...(~2.5Gb)"
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_esit.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_esro.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_fres.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_frit.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_frro.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_ptes.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_ptfr.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_ptit.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_ptro.t7
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/model_roit.t7

    echo "Downloading BPEs..."
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/ptes.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/ptfr.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/ptit.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/ptro.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/roit.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/fres.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/frit.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/frro.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/esit.bpe32000
    wget http://54.203.198.53:7000/Translation/OpenNMT/Romance/esro.bpe32000

    cd ..
fi

OPENNMT_PATH="./OpenNMT"
if [ ! -d "$OPENNMT_PATH" ]
then
    echo "Setting up OpenNMT..."
    git clone https://github.com/OpenNMT/OpenNMT.git
    # Make symlinks to access OpenNMT scripts - change this line if needed
    [ ! -h tools ] && ln -s $OPENNMT_PATH/tools tools
    [ ! -h preprocess.lua ] && ln -s $OPENNMT_PATH/preprocess.lua preprocess.lua
    [ ! -h train.lua ] && ln -s $OPENNMT_PATH/train.lua train.lua
    [ ! -h translate.lua ] && ln -s $OPENNMT_PATH/translate.lua translate.lua
    [ ! -h onmt ] && ln -s $OPENNMT_PATH/onmt onmt
fi