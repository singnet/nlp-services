import path_setup
import compile_proto
from services import named_entity_recognition as ner
from test_data import test_sentences
from log import log_config
logger = log_config.getLogger('run_unit_test.py', test=True)


class Request(object):
    def __init__(self):
        self.value = ""


def test_compiled():
    assert compile_proto.success


def test_recognize():
    """
    Test Named Entity Recognition
    :return:
    """

    servicer = ner.RecognizeMessageServicer()
    request = Request()
    request.value = test_sentences.senteces()
    context = object()
    response = servicer.Recognize(request, context)

    if "PERSON" in str(response.value) or "ORGANIZATION" in str(response.value) or "LOCATION" in str(response.value):
        logger.debug("test_recognize() - OK")
        assert True
    else:
        assert False, "Generated result is not valid"


path_setup.clean_paths()