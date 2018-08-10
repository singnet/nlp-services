# Text Summarization

This repository contains a SingularityNET service to do summarization of articles.

The current approach is that of [Get To The Point: Summarization with Pointer-Generator Networks](https://arxiv.org/pdf/1704.04368.pdf),
as implemented by OpenNMT.

There are a number of other methods that may of interest. So we may implement separate services for each,
while at the same keeping the interface the same (as much as possible)

pip install -r opennmt-py/requirements.txt
pip install numpy -I


python translate.py -gpu 0 \
                    -batch_size 20 \
                    -beam_size 5 \
                    -model ../models/gigaword_nocopy_acc_51.33_ppl_12.74_e20.pt \
                    -src ~/data/cnndm/test.txt.src \
                    -output cnndm.out \
                    -min_length 35 \
                    -verbose \
                    -stepwise_penalty \
                    -coverage_penalty summary \
                    -beta 5 \
                    -length_penalty wu \
                    -alpha 0.9 \
                    -verbose \
                    -block_ngram_repeat 3 \
                    -ignore_when_blocking "." "</t>" "<t>"

python translate.py -gpu 0 -batch_size 10 -beam_size 5 \
    -model ../models/sum_transformer_model_acc_57.25_ppl_9.22_e16.pt \
    -src ~/data/cnndm/test.txt.src \
    -output cnndm.out \
    -min_length 35 \
    -verbose \
    -stepwise_penalty \
    -coverage_penalty summary \
    -beta 5 \ 
    -length_penalty wu \
    -alpha 0.9 \
    -verbose \
    -block_ngram_repeat 3 \
    -ignore_when_blocking "." "</t>" "<t>" \
    -replace_unk

How to tokenize input?

Original CNN Daily Mail data here http://cs.nyu.edu/~kcho/DMQA/

Tokenization is described here, but relies on java library annoyingly
https://github.com/OpenNMT/cnn-dailymail
forked from https://github.com/abisee/cnn-dailymail - which converts straight into tensorflow binaries

java library - download CoreNLP (just the main JAR? or models too?)
https://stanfordnlp.github.io/CoreNLP/index.html

With some work, this pure python might be proven similar enough https://pypi.org/project/tokenizer/

