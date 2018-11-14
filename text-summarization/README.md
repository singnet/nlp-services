# Text Summarization

This repository contains a SingularityNET service to do summarization of articles.

The current approach is that of [Get To The Point: Summarization with Pointer-Generator Networks](https://arxiv.org/pdf/1704.04368.pdf),
as implemented by OpenNMT.

There are a number of other methods that may of interest. So we may implement separate services for each,
while at the same keeping the interface the same (as much as possible)

## Setup

These steps are run on Ubuntu 18.04, if you use a different distro/OS, the specifics may be different.

OpenNMT-py is a submodule, so you should clone the `nlp-services` repo with `--recurse-submodules`

```
git clone --recurse-submodules -j8 git@github.com:singnet/nlp-services.git
```

Now install the python dependencies for both OpenNMT and this project. Numpy is explicitly installed, as I ran into an error
with the version from opennmt-py's requirements.

```
cd nlp-services/text-summarization
mkvirtualenv --python=/usr/bin/python3.6 text-summarization
pip install -r opennmt-py/requirements.txt
pip install numpy -I
pip install -r requirements.txt
```

Last, you need to download the trained transformer model for summarization ([details](http://opennmt.net/Models-py/)) and
the Stanford CoreNLP java library. While an external java library is clunky, it was used as the tokenizer while training the model.
We use it to tokenize new user input to avoid differences in tokenization algorithms affecting results.

```
python ../fetch_models.py
```

The above will download archives and extract to the `nlp-services/text-summarization/models` directory.

## Running the server and making calls

Start the server with:

```
python -m services.summary_server
```

In another terminal, make a request to summarize an article with:

```
$ python client.py --source-text example_article.txt
 Senior National Collins is standing by her tweet of a fake news story. she says she had got her "sourcing" wrong, insisting it had some details wrong.
```

## OpenNMT Notes

In its current state OpenNMT is biased towards command line usage. These commands, to be run in the opennmt-py directory, were useful for initially experimenting with
the summarization models.

You will need to first download models from the [opennmt-py model page](http://opennmt.net/Models-py/).

```
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
```

```
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
```

### Data

Original CNN Daily Mail data here http://cs.nyu.edu/~kcho/DMQA/

These repos have preprocessing code, including tokenization using CoreNLP:
- https://github.com/OpenNMT/cnn-dailymail - fork, converts to text records
- https://github.com/abisee/cnn-dailymail - original, converts straight into tensorflow binaries

Tokenization is done by Stanford's Java library [CoreNLP](https://stanfordnlp.github.io/CoreNLP/index.html)

## License

MIT