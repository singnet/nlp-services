import sys
import logging
import base64
import io
import os
import argparse
import grpc
import time
import concurrent.futures
from multiprocessing import Pool

# Torch needs to be imported before sentencepiece otherwise segfault
# https://github.com/pytorch/pytorch/issues/8358
import torch

import sentencepiece as spm

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(ROOT_DIR, 'opennmt-py'))

from onmt.translate.translator import build_translator
import onmt.opts

from services import translations
from services import registry
import services.service_spec.translate_pb2 as ss_pb
import services.service_spec.translate_pb2_grpc as ss_grpc 


log = logging.getLogger(__package__ + "." + __name__)


class TranslationServicer(ss_grpc.TranslationServicer):
    def __init__(self, q):
        self.q = q
        pass

    def translate(self, request, context):
        print("blah")
        # text = kwargs.get("text", None)
        # source = kwargs.get("source", None)
        # target = kwargs.get("target", None)

        # if text is None:
        #     raise InvalidParams("text param is required")

        # if source not in translations:
        #     raise InvalidParams("source param must be one of", translations.keys())

        # if target not in translations[source]:
        #     raise InvalidParams("target param must be one of", translations[source].keys())

        self.q.send((request,))
        result = self.q.recv()
        print("result", result)
        if isinstance(result, Exception):
            raise result
        pb_result = ss_pb.Result(translation=result)

        return pb_result

def _translate(tokenized, translate_model):
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


def translate_text(text, source, target):
    if source == target:
        # The easy case ;-)
        return text

    t = translations[source][target]
    s = spm.SentencePieceProcessor()
    s.Load(os.path.join(ROOT_DIR, 'models', t["sentencepiece_model"]))
    pieces = s.encode_as_pieces(text)

    # add final full stop to ensure we don't lose any trailing words.
    if pieces[-1] != ".":
        pieces.append(".")

    indices = [i for i, _x in enumerate(pieces) if _x == "."]
    complete_result = []
    start=0
    for i in indices:
        x = " ".join([e for e in pieces[start:i+1]])
        result = _translate(x, translate_model=t['translate_model'])
        y = s.decode_pieces(result[1][0].split(" "))
        complete_result.append(y)
        start = i
    return "\n".join(complete_result)


def serve(dispatch_queue, max_workers=1, port=7777):
    assert max_workers == 1, "No support for more than one worker"
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=max_workers))
    ss_grpc.add_TranslationServicer_to_server(TranslationServicer(dispatch_queue), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


def main_loop(dispatch_queue, grpc_serve_function, grpc_port, grpc_args={}):
    server = None
    if grpc_serve_function is not None:
        server = grpc_serve_function(dispatch_queue, port=grpc_port, **grpc_args)
        server.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        server.stop(0)

def worker(q):
    while True:
        try:
            item = q.recv()
            with Pool(1) as p:
                result = p.apply(translate_text, (item[0].text, item[0].source_language, item[0].target_language))
            q.send(result)
        except Exception as e:
            q.send(e)


if __name__ == "__main__":
    script_name = __file__
    parser = argparse.ArgumentParser(prog=script_name)
    server_name = os.path.splitext(os.path.basename(script_name))[0]
    parser.add_argument("--grpc-port", help="port to bind grpc services to", default=registry[server_name]['grpc'], type=int, required=False)
    args = parser.parse_args(sys.argv[1:])

    # Need queue system and spawning grpc server in separate process because of:
    # https://github.com/grpc/grpc/issues/16001

    import multiprocessing as mp
    pipe = mp.Pipe()
    p = mp.Process(target=main_loop, args=(pipe[0], serve, args.grpc_port))
    p.start()

    w = mp.Process(target=worker, args=(pipe[1],))
    w.start()

    p.join()
    w.join()