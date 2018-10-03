import path_setup
import base64
import compile_proto
from services import named_entity_recognition as ner
from test_data import b64_sentences
from log import log_config
logger = log_config.getLogger('unity_test_service.py', test=True)


class Request(object):
    def __init__(self):
        self.value = ""


def test_compiled():
    assert compile_proto.success


def test_show():
    """
    Test calling show method
    :return:
    """

    servicer = ner.ShowMessageServicer()
    request = Request()
    request.value = 'Some input message'
    context = object()
    response = servicer.Show(request, context)

    if len(response.value) > 10:
        logger.debug("test_show() - OK")
        assert True
    else:
        assert False, "Call service error"


def test_recognize():
    """
    Test Named Entity Recognition
    :return:
    """

    servicer = ner.RecognizeMessageServicer()
    request = Request()
    request.value = b64_sentences.senteces()
    context = object()
    response = servicer.Recognize(request, context)
    decoded_result = base64.b64decode(response.value).decode('utf-8')

    if "PERSON" in str(decoded_result) or "ORGANIZATION" in str(decoded_result) or "LOCATION" in str(decoded_result):
        logger.debug("test_recognize() - OK")
        assert True
    else:
        assert False, "Generated result is not valid"

path_setup.clean_paths()