import sys
import logging
import argparse
import os
import grpc
import concurrent.futures
import time
from multiprocessing import Pool

from services import registry
from services.onmt_utils import stanford_ptb_detokenizer, stanford_ptb_tokenizer, summary
import services.service_spec.summary_pb2 as ss_pb
import services.service_spec.summary_pb2_grpc as ss_grpc 


log = logging.getLogger(__package__ + "." + __name__)


class TextSummaryServicer(ss_grpc.TextSummaryServicer):
    def __init__(self, q):
        self.q = q
        pass

    def summary(self, request, context):
        self.q.send((request.article_content,))
        result = self.q.recv()
        if isinstance(result, Exception):
            raise result
        print(result)
        pb_result = ss_pb.Result(article_summary=result)
        return pb_result


def summarise_text(text):
    tokens = stanford_ptb_tokenizer(text)
    score, p = summary(tokens)
    result = p[0].replace(' <t>', '').replace(' </t>', '').replace('<t>', '')
    return stanford_ptb_detokenizer(result)


def serve(dispatch_queue, max_workers=1, port=7777):
    assert max_workers == 1, "No support for more than one worker"
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=max_workers))
    ss_grpc.add_TextSummaryServicer_to_server(TextSummaryServicer(dispatch_queue), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


def main_loop(dispatch_queue, grpc_serve_function, grpc_port, grpc_args=None):
    if grpc_args is None:
        grpc_args = dict()

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
                result = p.apply(summarise_text, (item[0],))
            q.send(result)
        except Exception as e:
            q.send(e)


if __name__ == "__main__":
    script_name = __file__
    parser = argparse.ArgumentParser(prog=script_name)
    server_name = os.path.splitext(os.path.basename(script_name))[0]
    parser.add_argument("--grpc-port",
                        help="port to bind grpc services to",
                        default=registry[server_name]['grpc'],
                        type=int,
                        required=False)
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
