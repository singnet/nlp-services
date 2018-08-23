import asyncio
import argparse
import os.path

from aiohttp import web

from services import registry


def common_parser(script_name):
    parser = argparse.ArgumentParser(prog=script_name)
    server_name = os.path.splitext(os.path.basename(script_name))[0]
    parser.add_argument("--grpc-port", help="port to bind grpc services to", default=registry[server_name]['grpc'], type=int, required=False)
    parser.add_argument("--json-rpc-port", help="port to bind jsonrpc services to", default=registry[server_name]['jsonrpc'], type=int,
                        required=False)
    return parser


async def _start_json_rpc(runner, host, port):
    await runner.setup()
    site = web.TCPSite(runner, str(host), port)
    await site.start()

    while True:
        await asyncio.sleep(1)


def main_loop(grpc_serve_function, grpc_args, jsonrpc_handler, args):
    server = None
    if grpc_serve_function is not None:
        server = grpc_serve_function(port=args.grpc_port, **grpc_args)
        server.start()

    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    app.router.add_post('/', jsonrpc_handler)
    runner = web.AppRunner(app)

    try:
        loop.run_until_complete(_start_json_rpc(runner, host="127.0.0.1", port=args.json_rpc_port))
    except KeyboardInterrupt:
        if server is not None:
            server.stop(0)
        loop.run_until_complete(runner.cleanup())

    loop.close()
