import sys
import subprocess
import os
import argparse

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(ROOT_DIR, 'opennmt-py'))

import torch
from onmt.translate.translator import build_translator
import onmt.opts


def stanford_tokenizer(text):
    os.environ["CLASSPATH"] = os.path.join(ROOT_DIR, "models/stanford-corenlp-full-2018-01-31/stanford-corenlp-3.9.0.jar")

    command = ['java', 'edu.stanford.nlp.process.PTBTokenizer', '-preserveLines']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(input=text.encode())
    if p.returncode != 0:
        raise Exception("Failed to tokenize", err)
    return out.decode()


def summary(tokenized):
    summary_model = 'sum_transformer_model_acc_57.25_ppl_9.22_e16.pt'

    # OpenNMT is awkwardly designed which makes it annoying to programmatic load a model.
    # Their server uses this appraoch to load a model by manipulating the command
    # line arguments, parsing, and then restoring them.
    parser = argparse.ArgumentParser()
    onmt.opts.translate_opts(parser)

    prec_argv = sys.argv
    sys.argv = sys.argv[:1]

    opt = {
        'batch_size': 1,
        'beam_size': 15,
        'min_length': 35,
        'verbose': True,
        'stepwise_penalty': True,
        'coverage_penalty': 'summary',
        'beta': 5,
        'length_penalty': 'wu',
        'alpha': 0.9,
        'verbose': True, 
        'block_ngram_repeat': 3,
        'ignore_when_blocking': "." "</t>" "<t>",
        'replace_unk': True,
        'gpu': 0
    }
    opt['model'] = os.path.join(ROOT_DIR, 'models', summary_model)
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

    return scores[0], predictions[0]