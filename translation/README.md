# Language Translation

This repository contains a SingularityNET service to translate between a limited subset of languages.

Currently we support English <-> German.

We use OpenNMT-py and Google's Transformer network.

## Setup

OpenNMT-py is a submodule, so you should clone the `nlp-services` repo with `--recurse-submodules`

```
git clone --recurse-submodules -j8 git@github.com:singnet/nlp-services.git
```

Now install the python dependencies for both OpenNMT and this project. Numpy is explicitly installed, as I ran into an error
with the version from opennmt-py's requirements.

```
pip install -r nlp-services/text-summarization/opennmt-py/requirements.txt
pip install numpy -I
cd nlp-services/translation
pip install -r requirements.txt
```

Last, you need to download the trained transformer models for translation.
Details of each model are in `services/__init__.py`

```
python fetch_models.py
```

The above will download archives and extract to the `nlp-services/translation/models` directory.

## Testing locally

A script that does what the service does and tests if the model/tokenization setup is working okay is available in the translate.py script

```
python translate.py
```

## OpenNMT Notes

To translate `en->de`

The provided model expects and provides sentences tokenized with Google's sentencepiece

```
>>> import sentencepiece as spm
>>> s = spm.SentencePieceProcessor()
>>> s.Load('models/en_de_sp.model')
>>> x = s.encode_as_pieces(u'This is a sentence.'); print(x)
[b'\xe2\x96\x81I', b'\xe2\x96\x81like', b'\xe2\x96\x81the', b'\xe2\x96\x81but', b't', b's']
>>> x = " ".join([e.decode('utf-8') for e in x])); print(x)
▁This ▁is ▁a ▁sentence .
>>> y = s.decode_pieces(x.split(" "))
>>> print(y.decode('utf-8'))
```

Save the utf-8 decoded string to a file. One sentence per line.

To translate, from the opennmt-py dir:

```
python translate.py -gpu 0 -model  ../../translation/models/en_to_de_omnt_averaged_10_epoch.pt -src my_sentencepiece_output.txt -replace_unk -verbose -output my_output
```

The result will be in `my_output`

### Data

OpenNMT trains their models on parts of the [Corpus provided for the WMT translation task](http://www.statmt.org/wmt18/translation-task.html).