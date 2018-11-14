import sys
import os
import io
import grpc
import argparse

from services.snet import snet_setup
from services import registry

import services.service_spec.translate_pb2_grpc as grpc_bt_grpc
import services.service_spec.translate_pb2 as grpc_bt_pb2

SERVER_NAME = 'translate_server'

def main():
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=script_name)
    default_endpoint = "127.0.0.1:{}".format(registry[SERVER_NAME]['grpc'])
    parser.add_argument("--endpoint", help="grpc server to connect to", default=default_endpoint,
                        type=str, required=False)
    parser.add_argument("--snet", help="call service on SingularityNet - requires configured snet CLI",
                        action='store_true')
    parser.add_argument("--source-text", help="path to txt file to translate",
                        type=str, required=True)
    parser.add_argument("--source-language", help="language to tranlate from",
                        type=str, required=True)
    parser.add_argument("--target-language", help="language to tranlate to",
                        type=str, required=True)
    args = parser.parse_args(sys.argv[1:])

    endpoint = args.endpoint

    valid_sources = ['en', 'de']
    valid_targets = ['en', 'de']

    if args.source_language not in valid_sources:
        print("Source language must be one of ", valid_sources)
        return 1
    if args.target_language not in valid_targets:
        print("Source language must be one of ", valid_targets)
        return 1
    if args.target_language == args.source_language:
        print("Source and target language is the same!")
        return 1

    with open(args.source_text, 'r') as f:
        text = f.read()

    channel = grpc.insecure_channel("{}".format(args.endpoint))
    stub = grpc_bt_grpc.TranslationStub(channel)

    request = grpc_bt_pb2.Request(text=text, source_language=args.source_language, target_language=args.target_language)

    metadata = []
    if args.snet:
        endpoint, job_address, job_signature = snet_setup(service_name="translation", max_price=10000000)
        metadata = [("snet-job-address", job_address), ("snet-job-signature", job_signature)]

    response = stub.translate(request, metadata=metadata)
    print(response.translation)

    return 0


if __name__ == '__main__':
    result = main()
    sys.exit(result)