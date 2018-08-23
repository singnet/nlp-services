import sys
import logging
import base64
import io
import os

from services.onmt_utils import stanford_ptb_detokenizer, stanford_ptb_tokenizer, summary

from aiohttp import web
from jsonrpcserver.aio import methods
from jsonrpcserver.exceptions import InvalidParams

import services.common


log = logging.getLogger(__package__ + "." + __name__)


def summarise_text(text):
    tokens = stanford_ptb_tokenizer(text)
    score, p = summary(tokens)
    result = p[0].replace(' <t>', '').replace(' </t>', '').replace('<t>', '')
    return stanford_ptb_detokenizer(result)


@methods.add
async def ping():
    return 'pong'


@methods.add
async def summarise(**kwargs):
    text = kwargs.get("text", None)

    if text is None:
        raise InvalidParams("text is required")

    from multiprocessing import Pool
    global config
    with Pool(1) as p:
        result = p.apply(summarise_text, (text,))

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