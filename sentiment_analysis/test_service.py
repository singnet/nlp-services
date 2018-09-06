import grpc

# import the generated classes
from services.model import sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
from services.model import sentiment_analysis_rpc_pb2 as grpc_bt_pb2
from test_data import b64_sentences
from test_data import twitter_credentials
from services import registry
from log import log_config

logger = log_config.getLogger('test_service.py')

if __name__ == '__main__':

    try:
        logger.debug('call => __name == __main__')

        logger.debug("call => ShowMessage() Method Test Starting... ")
        print()
        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

        # ShowMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.ShowMessageStub(channel)
        # create a valid request message
        test_text = "RODANDO TESTES..."
        message = grpc_bt_pb2.InputMessage(value=test_text)
        # make the call
        response = stub.show(message)
        logger.debug("call => ShowMessage() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    # try:
    #     logger.debug("call => SentimentIntensityAnalysis() Method Test Starting... ")
    #     print()
    #     # SentimentIntensityAnalysis() Method Test
    #     # create a stub (client)
    #     stub = grpc_bt_grpc.SentimentIntensityAnalysisStub(channel)
    #     # create a valid request message
    #     test_data = b64_sentences.senteces()
    #     message = grpc_bt_pb2.InputMessage(value=test_data)
    #     # make the call
    #     response = stub.intensivityAnalysis(message)
    #     logger.debug("call => SentimentIntensityAnalysis() Method Test Passed => " + response.value)
    #     print()
    #
    # except KeyError as e:
    #     print(e)
    #
    # try:
    #
    #     logger.debug("call => SentimentComplexAnalysis() Method Test Starting... ")
    #     print()
    #     # SentimentComplexAnalysis() Method Test
    #     # create a stub (client)
    #     stub = grpc_bt_grpc.SentimentComplexAnalysisStub(channel)
    #     # create a valid request message
    #     test_data = b64_sentences.senteces()
    #     message = grpc_bt_pb2.InputMessage(value=test_data)
    #     # make the call
    #     response = stub.complexAnalysis(message)
    #     logger.debug("call => SentimentComplexAnalysis() Method Test Passed => " + response.value)
    #     print()
    #
    # except KeyError as e:
    #     print(e)

    try:

        # logger.debug("CustomCorpusAnalysis() Method Test Starting... ")
        # print()
        # # CustomCorpusAnalysis() Method Test
        # # create a stub (client)
        # stub = grpc_bt_grpc.CustomCorpusAnalysisStub(channel)
        # # create a valid request message
        # test_text = "RODANDO TESTES..."
        # message = grpc_bt_pb2.InputMessage(value=test_text)
        # # make the call
        # response = stub.show(message)
        # logger.debug("CustomCorpusAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    # try:
    #
    #     logger.debug("call => TwitterStreamAnalysis() Method Test Starting... ")
    #     print()
    #     # TwitterStreamAnalysis() Method Test
    #     # create a stub (client)
    #     stub = grpc_bt_grpc.TwitterStreamAnalysisStub(channel)
    #
    #     # Setting the credentials up
    #     credentials = grpc_bt_pb2.TwitterCredentials(consumer_key=twitter_credentials.consumer_key,
    #                                                  consumer_secret=twitter_credentials.consumer_secret,
    #                                                  access_token=twitter_credentials.access_token,
    #                                                  token_secret=twitter_credentials.token_secret)
    #     # Setting the input message up
    #     message = grpc_bt_pb2.TwitterInputMessage(
    #         credentials=credentials,
    #         languages=twitter_credentials.languages,
    #         sentences=twitter_credentials.sentences,
    #         time_limit=twitter_credentials.time_limit,
    #         msg_limit=twitter_credentials.msg_limit)
    #
    #     # make the call
    #     response = stub.streamAnalysis(message)
    #     logger.debug("call => TwitterStreamAnalysis() Method Test Passed => " + response.value)
    #     print()
    #
    # except KeyError as e:
    #     logger.debug("call => TwitterStreamAnalysis() Method Test Error => " + str(e))
