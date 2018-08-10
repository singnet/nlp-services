import sys
import logging
import base64
import io
import os

import torch
import onmt.opts

from onmt.utils.logging import init_logger
from onmt.translate.translator import build_translator

from aiohttp import web
from jsonrpcserver.aio import methods
from jsonrpcserver.exceptions import InvalidParams

import services.common


log = logging.getLogger(__package__ + "." + __name__)


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")


def init():
    sys.path.append(os.path.join(ROOT_DIR, "opennmt-py"))


def load_model():
    log.info("Loading model")
    opt = None
    tokenizer_opt = None

    translator = build_translator(opt, report_score=False, out_file=open(os.devnull, "w"))

    model_root = None

    log.info("Loading tokenizer")
    mandatory = ["type", "model"]
    for m in mandatory:
        if m not in tokenizer_opt:
            raise ValueError("Missing mandatory tokenizer option '%s'" % m)
    if tokenizer_opt['type'] == 'sentencepiece':
        import sentencepiece as spm
        sp = spm.SentencePieceProcessor()
        model_path = os.path.join(model_root, tokenizer_opt['model'])
        sp.Load(model_path)
        self.tokenizer = sp
    elif self.tokenizer_opt['type'] == 'bpe_onmt_tokenizer':
        import pyonmttok
        model_path = os.path.join(self.model_root,
                                    self.tokenizer_opt['model'])
        tokenizer = pyonmttok.Tokenizer(
            "aggressive",
            bpe_model_path=model_path,
            joiner_annotate=True,
            joiner_new=True,
            preserve_placeholders=True)
        self.tokenizer = tokenizer
    else:
        raise ValueError("Invalid value for tokenizer type")

    self.load_time = timer.tick()
    self.reset_unload_timer()

def run(self, inputs):
    """Translate `inputs` using this model

        Args:
            inputs: [{"src": "..."},{"src": ...}]

        Returns:
            result: (list) translations
            times: (dict) containing times
    """
    timer = Timer()
    self.logger.info("\nRunning translation using %d" % self.model_id)

    timer.start()
    if not self.loaded:
        self.load()
        timer.tick(name="load")
    elif self.opt.cuda:
        self.to_gpu()
        timer.tick(name="to_gpu")

    texts = []
    whitespace_segments = {}
    subsegment = {}
    sscount = 0
    sslength = []
    for (i, inp) in enumerate(inputs):
        src = inp['src']
        lines = src.split("\n")
        subsegment[i] = slice(sscount, sscount + len(lines))
        for line in lines:
            tok = self.maybe_tokenize(line)
            if len(''.join(line.split())) == 0:
                whitespace_segments[sscount] = line
                sscount += 1
            else:
                texts += [tok]
                sslength += [len(tok.split())]
                sscount += 1

    timer.tick(name="writing")

    scores = []
    predictions = []
    if sscount > 0:
        try:
            scores, predictions = self.translator.translate(
                src_data_iter=texts, batch_size=self.opt.batch_size)
        except RuntimeError as e:
            raise ServerModelError("Runtime Error: %s" % str(e))

    timer.tick(name="translation")
    self.logger.info("""Using model #%d\t%d inputs (%d subsegment)
            \ttranslation time: %f""" % (self.model_id, len(subsegment),
                                        sscount,
                                        timer.times['translation']))
    self.reset_unload_timer()

    # NOTE: translator returns lists of `n_best` list
    #       we can ignore that (i.e. flatten lists) only because
    #       we restrict `n_best=1`
    def flatten_list(_list): return sum(_list, [])
    results = flatten_list(predictions)
    scores = [score_tensor.item()
                for score_tensor in flatten_list(scores)]

    self.logger.info("Translation Results: %d", len(results))
    if len(whitespace_segments) > 0:
        self.logger.info("Whitespace segments: %d"
                            % len(whitespace_segments))

    for k in sorted(whitespace_segments.keys()):
        results.insert(k, whitespace_segments[k])
        scores.insert(k, 0.0)

    results = ['\n'.join([self.maybe_detokenize(_)
                            for _ in results[subsegment[i]]])
                for i in sorted(subsegment.keys())]

    avg_scores = [sum([s * l for s, l in zip(scores[sub], sslength[sub])])
                    / sum(sslength[sub])
                    if sum(sslength[sub]) != 0 else 0.0
                    for k, sub
                    in sorted(subsegment.items(), key=lambda x: x[0])]

    return results, avg_scores, self.opt.n_best, timer.times


def summarise_text(text):
    model = load_model()
    r = model.predict(text)
    del model
    return r


@methods.add
async def ping():
    return 'pong'


@methods.add
async def summarise(**kwargs):
    image = kwargs.get("text", None)

    if image is None:
        raise InvalidParams("text is required")

    from multiprocessing import Pool
    global config
    with Pool(1) as p:
        result = p.apply(summarise_text, (img,))

    # TODO support top 5 summarise from beam search?
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
    init()
    services.common.main_loop(None, None, handle, args)