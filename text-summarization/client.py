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
    parser.add_argument("--source-text", help="path to txt file to summarise",
                        type=str, required=True)
    args = parser.parse_args(sys.argv[1:])

    endpoint = args.endpoint

    with open(args.source_text, 'r') as f:
        text = f.read()
    params = {'text': text}
    if args.snet:
        endpoint, job_address, job_signature = snet_setup(service_name="text_summarization", max_price=10000000)
        params['job_address'] = job_address
        params['job_signature'] = job_signature

    response = jsonrpcclient.request(endpoint, "summarise", **params)
    print(response)



if __name__ == '__main__':
    main()
