# import path_setup
import compile_proto
from services import sentiment_analysis as analysis
from log import log_config
logger = log_config.getLogger('unity_test_service.py', test=True)


class message(object):
    def __init__(self):
        self.value = ""


class TwitterApiReaderMessage:
    def __init__(self):
        self.consumer_key = request.credentials.consumer_key,
        self.consumer_secret = request.credentials.consumer_secret,
        self.access_token = request.credentials.access_token,
        self.token_secret = request.credentials.token_secret,
        self.msg_limit = 0,
        self.time_limit = 0,
        self.max_requests_limit = 0,
        self.db_name = None


def test_compiled():
    assert compile_proto.success


def test_show():
    """
    Test calling show method
    :return:
    """

    servicer = analysis.ShowMessageServicer()
    request = message()
    # request = object()
    context = object()
    # setattr(request, 'value', 'Testando')
    request.value = 'Testando'
    response = servicer.Show(request, context)
    if len(response.value) > 10:
        logger.debug("test_show() - OK")
    assert len(response.value) > 10, "Call service error"


# def test_ConsensusAnalysis():
#     """
#     Test Consensus Analysis
#     :return:
#     """
#
#     servicer = analysis.TwitterHistoricalAnalysisServicer()
#     request = message()
#     context = object()
#     request.value = 'Testando'
#     response = servicer.HistoricalAnalysis(resquest, context)
#
#     # Create a stub (client)
#     stub = grpc_services.SentimentConsensusAnalysisStub(get_channel())
#     # Load test data
#     test_data = b64_sentences.senteces()
#     # Setting the input message up
#     message = rpc.InputMessage(value=test_data)
#     # Call the method
#     response = stub.ConsensusAnalysis(message)
#     response_text = base64.b64decode(response.value).decode('utf-8')
#     assert "pos" in str(response_text) or "neg" in str(response_text), "Generated result is not valid!"
#
#
# def test_hisorical_analysis():
#     """
#     Test Historical Analysis
#     :return:
#     """
#     # create a stub (client)
#     stub = grpc_services.TwitterHistoricalAnalysisStub(get_channel())
#
#     # Setting the credentials up
#     credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
#                                                  consumer_secret=twitter_test_data.consumer_secret,
#                                                  access_token=twitter_test_data.access_token,
#                                                  token_secret=twitter_test_data.token_secret)
#     # Setting the input message up
#     message = rpc.TwitterInputMessage(
#         credentials=credentials,
#         languages=twitter_test_data.languages,
#         query=twitter_test_data.query,
#         product=twitter_test_data.product,
#         environment=twitter_test_data.environment,
#         from_date=twitter_test_data.fromDate,
#         to_date=twitter_test_data.toDate,
#         messages_per_request=twitter_test_data.messages_per_request)
#
#     # Call the method
#     response = stub.HistoricalAnalysis(message)
#     response_text = base64.b64decode(response.value).decode('utf-8')
#     assert "pos" in str(response_text) or "neg" in str(response_text), "Generated result is not valid!"
#
#
# def historical_analysis_database():
#     """
#     Test Historical Analysis to Database
#     :return:
#     """
#
#     # create a stub (client)
#     stub = grpc_services.TwitterHistoricalAnalysisStub(get_channel())
#
#     # Setting the credentials up
#     credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
#                                                  consumer_secret=twitter_test_data.consumer_secret,
#                                                  access_token=twitter_test_data.access_token,
#                                                  token_secret=twitter_test_data.token_secret)
#     # Setting the input message up
#     message = rpc.TwitterInputMessage(
#         credentials=credentials,
#         languages=twitter_test_data.languages,
#         query=twitter_test_data.query,
#         product=twitter_test_data.product,
#         environment=twitter_test_data.environment,
#         from_date=twitter_test_data.fromDate,
#         to_date=twitter_test_data.toDate,
#         messages_per_request=twitter_test_data.messages_per_request,
#         max_requests_limit=twitter_test_data.max_requests_limit,
#         db_name=twitter_test_data.db_name)
#
#     # Call the method
#     response = stub.HistoricalAnalysisToDatabase(message)
#     response_text = base64.b64decode(response.value).decode('utf-8')
#     print(response_text)
#     assert "pos" in str(response_text) or "neg" in str(response_text), "Generated result is not valid!"
#
#
# def test_stream_analysis():
#     """
#     Test Stream Analysis
#     :return:
#     """
#
#     # create a stub (client)
#     stub = grpc_services.TwitterStreamAnalysisStub(get_channel())
#
#     # Setting the credentials up
#     credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
#                                                  consumer_secret=twitter_test_data.consumer_secret,
#                                                  access_token=twitter_test_data.access_token,
#                                                  token_secret=twitter_test_data.token_secret)
#     # Setting the input message up
#     message = rpc.TwitterInputMessage(
#         credentials=credentials,
#         languages=twitter_test_data.languages,
#         query=twitter_test_data.query,
#         time_limit=twitter_test_data.time_limit,
#         msg_limit=twitter_test_data.msg_limit)
#
#     # Call the method
#     response = stub.StreamAnalysis(message)
#     response_text = base64.b64decode(response.value).decode('utf-8')
#     assert "pos" in str(response_text) or "neg" in str(response_text), "Generated result is not valid!"

# path_setup.clean_paths()