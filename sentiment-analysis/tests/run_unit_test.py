import path_setup
import base64
import compile_proto
from services import sentiment_analysis as analysis
from test_data import test_sentences
from log import log_config
logger = log_config.getLogger('unit_test_service.py', test=True)


class Message(object):
    def __init__(self):
        self.value = ""


def test_compiled():
    assert compile_proto.success


def test_analyze():
    """
    Test Sentiment Analysis
    :return:
    """

    servicer = analysis.SentimentAnalysisServicer()
    request = Message()
    request.value = test_sentences.senteces()
    context = object()
    response = servicer.Analyze(request, context)
    logger.debug(response.value)
    assert "pos" in str(response.value) or "neg" in str(response.value), "Generated result is not valid!"


path_setup.clean_paths()