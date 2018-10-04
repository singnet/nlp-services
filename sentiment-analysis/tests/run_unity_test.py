import path_setup
import json
import base64
import compile_proto
from services.modules import twitter_mod
from services import sentiment_analysis as analysis
from test_data import b64_sentences
from log import log_config
logger = log_config.getLogger('unity_test_service.py', test=True)


class Message(object):
    def __init__(self):
        self.value = ""


def test_compiled():
    assert compile_proto.success


def test_show():
    """
    Test calling show method
    :return:
    """

    servicer = analysis.ShowMessageServicer()
    request = Message()
    request.value = 'Some input message'
    context = object()
    response = servicer.Show(request, context)
    logger.debug(response)
    assert len(response.value) > 10, "Call service error"


def test_consensus_analysis():
    """
    Test Consensus Analysis
    :return:
    """

    servicer = analysis.SentimentConsensusAnalysisServicer()
    request = Message()
    request.value = b64_sentences.senteces()
    context = object()
    response = servicer.ConsensusAnalysis(request, context)
    decoded_result = base64.b64decode(response.value).decode('utf-8')
    logger.debug(decoded_result)
    assert "pos" in str(decoded_result) or "neg" in str(decoded_result), "Generated result is not valid!"


def test_hisorical_analysis():
    """
    Test Historical Analysis
    :return:
    """

    with open('test_data/twitter_response_sample.json') as json_file:
        json_data = json.load(json_file)

        servicer = analysis.TwitterHistoricalAnalysisServicer()

        servicer.reader = twitter_mod.TwitterApiReader(consumer_key='3049855346398657943678',
                                                       consumer_secret='3049855346398657943678',
                                                       access_token='3049855346398657943678',
                                                       token_secret='3049855346398657943678',
                                                       product='30day',
                                                       environment='dev',
                                                       query='happy OR world peace',
                                                       messages_per_request=1,
                                                       max_requests_limit=1,
                                                       msg_limit=1,
                                                       time_limit=1,
                                                       from_date='201809260000',
                                                       to_date='201809260000',
                                                       db_name='db_name')

        servicer.reader.messages = []
        servicer.reader.messages.append(json_data['results'])
        result = servicer.twitter_reader_analysis(servicer.reader)
    logger.debug(result)
    assert "pos" in str(result) or "neg" in str(result), "Generated result is not valid!"


def test_stream_analysis():
    """
    Test Stream Analysis
    :return:
    """

    with open('test_data/twitter_response_sample.json') as json_file:
        json_data = json.load(json_file)

        servicer = analysis.TwitterStreamAnalysisServicer()

        servicer.manager = twitter_mod.SnetStreamManager(consumer_key='98675785875765',
                                                         consumer_secret='98675785875765',
                                                         access_token='98675785875765',
                                                         token_secret='98675785875765',
                                                         msg_limit=1,
                                                         time_limit=1)

        servicer.manager.stream.listener.sentences = [item['text'] for item in json_data['results']]
        servicer.twitter_manager_analysis(servicer.manager)
    logger.debug(servicer.stringResult)
    assert "pos" in str(servicer.stringResult) or "neg" in str(servicer.stringResult), "Generated result is not valid!"


path_setup.clean_paths()