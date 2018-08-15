#!/bin/bash
cd models
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-01-31.zip
unzip stanford-corenlp-full-2018-01-31.zip
export CLASSPATH=stanford-corenlp-full-2018-01-31/stanford-corenlp-3.9.1.jar

# command to test:
# echo "Please tokenize this text." | java edu.stanford.nlp.process.PTBTokenizer -preserveLines