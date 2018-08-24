import sys
import logging
import base64
import io
import os
import argparse

# Torch needs to be imported before sentencepiece otherwise segfault
# https://github.com/pytorch/pytorch/issues/8358
import torch

import sentencepiece as spm

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(ROOT_DIR, 'opennmt-py'))

from onmt.translate.translator import build_translator
import onmt.opts

from aiohttp import web
from jsonrpcserver.aio import methods
from jsonrpcserver.exceptions import InvalidParams

import services.common


log = logging.getLogger(__package__ + "." + __name__)


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

    del translator
    return scores[0], predictions[0]


def translate_text(text, source, target):
    if source == target:
        # The easy case ;-)
        return text

    t = translations[source_language][target_language]
    s = spm.SentencePieceProcessor()
    s.Load(os.path.join(ROOT_DIR, 'models', t["sentencepiece_model"])
    x = s.encode_as_pieces(text)
    complete_result = []
    for i in x.finditer(b'.'):
        i = x.index(b'.', x.index(b'.') + 1)
    
        x = " ".join([e.decode('utf-8') for e in x[:i+1]])
        result = translate(x, t['translate_model'])
        y = s.decode_pieces(result[1][0].split(" "))
        complete_result.append(y.decode('utf-8'))
    return "\n".join(complete_result)


@methods.add
async def ping():
    return 'pong'


@methods.add
async def translate(**kwargs):
    text = kwargs.get("text", None)
    source = kwargs.get("source", None)
    target = kwargs.get("target", None)

    if text is None:
        raise InvalidParams("text param is required")

    if source not in translations:
        raise InvalidParams("source param must be one of", translations.keys())

    if target not in translations[source]:
        raise InvalidParams("target param must be one of", translations[source].keys())

    from multiprocessing import Pool
    global config
    with Pool(1) as p:
        result = p.apply(translate_text, (text, source, target))

    return {'summary': result}


async def handle(request):
    request = await request.text()
    response = await methods.dispatch(request, trim_log_values=True)
    if response.is_notification:
        return web.Response()
    else:
        return web.json_response(response, status=response.http_status)


if __name__ == '__main__':
    parser = services.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    services.common.main_loop(None, None, handle, args)