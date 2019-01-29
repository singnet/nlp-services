### Basic translator to directly translate untokenized text.
import sys
import argparse
import os
# Torch needs to be imported before sentencepiece otherwise segfault
# https://github.com/pytorch/pytorch/issues/8358
import torch

import sentencepiece as spm

ROOT_DIR = os.path.join(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(ROOT_DIR, 'opennmt-py'))

from onmt.translate.translator import build_translator
import onmt.opts

# Dictionary mapping for what languages we know how to translate
from services import translations
from services.translate_server import translate_text


def translate(tokenized, translate_model):

    # OpenNMT is awkwardly designed which makes it annoying to programmatic load a model.
    # Their server uses this appraoch to load a model by manipulating the command
    # line arguments, parsing, and then restoring them.
    parser = argparse.ArgumentParser()
    onmt.opts.translate_opts(parser)

    prec_argv = sys.argv
    sys.argv = sys.argv[:1]

    opt = {
        'verbose': True,
        'replace_unk': True,
        'gpu': 0
    }
    opt['model'] = os.path.join(ROOT_DIR, 'models', translate_model)
    opt['src'] = "dummy_src"

    for (k, v) in opt.items():
        if type(v) == bool:
            sys.argv += ['-%s' % k]
        else:
            sys.argv += ['-%s' % k, str(v)]

    opt = parser.parse_args()
    opt.cuda = opt.gpu > -1
    sys.argv = prec_argv

    translator = build_translator(opt, report_score=False, out_file=open(os.devnull, "w"))

    scores = []
    predictions = []

    scores, predictions = translator.translate(src_data_iter=[tokenized], batch_size=1)

    del translator
    return scores[0], predictions[0]


if __name__ == "__main__":

    with open('example_de_article.txt', 'r') as f:
        text = f.read()

    # transations[from][to]
    source_language = "de"
    target_language = "en"

    print(translate_text(text, source_language, target_language))
