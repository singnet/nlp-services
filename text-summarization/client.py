import sys
import os
import io
import grpc
import argparse

from services.snet import snet_setup
from services import registry

import services.service_spec.summary_pb2_grpc as grpc_bt_grpc
import services.service_spec.summary_pb2 as grpc_bt_pb2

SERVER_NAME = 'summary_server'


def main():
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=script_name)

    default_endpoint = "127.0.0.1:{}".format(registry[SERVER_NAME]['grpc'])
    parser.add_argument("--endpoint", help="grpc server to connect to", default=default_endpoint,
                        type=str, required=False)
    parser.add_argument("--snet", help="call services on SingularityNet - requires configured snet CLI",
                        action='store_true')
    parser.add_argument("--source-text", help="path to txt file to summarise",
                        type=str, required=True)
    args = parser.parse_args(sys.argv[1:])

    channel = grpc.insecure_channel("{}".format(args.endpoint))
    stub = grpc_bt_grpc.TextSummaryStub(channel)

    with open(args.source_text, 'r') as f:
        text = f.read()

    request = grpc_bt_pb2.Request(article_content=text)

    metadata = []
    if args.snet:
        endpoint, job_address, job_signature = snet_setup(service_name="text_summarization", max_price=10000000)
        metadata = [("snet-job-address", job_address), ("snet-job-signature", job_signature)]

    response = stub.summary(request, metadata=metadata)
    print(response.article_summary)


if __name__ == '__main__':
    main()