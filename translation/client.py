import jsonrpcclient
import sys
import os
import argparse
import base64

from services.snet import snet_setup
from services import registry


def main():
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=script_name)
    server_name = "summary_server"
    default_endpoint = "http://127.0.0.1:{}".format(registry[server_name]['jsonrpc'])
    parser.add_argument("--endpoint", help="jsonrpc server to connect to", default=default_endpoint,
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
    params = {
        'text': text,
        'source': args.source_language,
        'target': args.target_language,
    }

    if args.snet:
        endpoint, job_address, job_signature = snet_setup(service_name="translation", max_price=10000000)
        params['job_address'] = job_address
        params['job_signature'] = job_signature

    response = jsonrpcclient.request(endpoint, "translate", **params)
    print(response)
    return 0


if __name__ == '__main__':
    result = main()
    sys.exit(result)