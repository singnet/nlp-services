import path_setup
import grpc
from services.service_spec import sentiment_analysis_rpc_pb2_grpc as grpc_services
from services.service_spec import sentiment_analysis_rpc_pb2 as rpc
from test_data import b64_sentences, twitter_test_data
from services import registry
from log import log_config

logger = log_config.getLogger('test_service.py', test=True)
channel = None

if __name__ == '__main__':

    try:
        logger.debug('call => __name == __main__')
        logger.debug("call => ShowMessage() Method Test Starting... ")
        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

    except KeyError as e:
        print(e)

    try:

        # ShowMessage() Method Test
        # create a stub (client)
        stub = grpc_services.ShowMessageStub(channel)
        # create a valid request message
        test_text = "some input message"
        message = rpc.InputMessage(value=test_text)
        # make the call
        response = stub.Show(message)
        logger.debug("call => ShowMessage() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:

        logger.debug("call => SentimentConsensusAnalysis() Method Test Starting... ")
        # SentimentConsensusAnalysis() Method Test
        # create a stub (client)
        stub = grpc_services.SentimentConsensusAnalysisStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = rpc.InputMessage(value=test_data)
        # make the call
        response = stub.ConsensusAnalysis(message)
        logger.debug("call => SentimentConsensusAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:

        logger.debug("call => TwitterHistoricalAnalysis() Method Test Starting... ")
        print()
        # TwitterHistoricalAnalysis() Method Test
        # create a stub (client)
        stub = grpc_services.TwitterHistoricalAnalysisStub(channel)

        # Setting the credentials up
        credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
                                                     consumer_secret=twitter_test_data.consumer_secret,
                                                     access_token=twitter_test_data.access_token,
                                                     token_secret=twitter_test_data.token_secret)
        # Setting the input message up
        message = rpc.TwitterInputMessage(
            credentials=credentials,
            languages=twitter_test_data.languages,
            query=twitter_test_data.query,
            product=twitter_test_data.product,
            environment=twitter_test_data.environment,
            from_date=twitter_test_data.fromDate,
            to_date=twitter_test_data.toDate,
            messages_per_request=twitter_test_data.messages_per_request)

        # make the call
        response = stub.HistoricalAnalysis(message)
        logger.debug("call => TwitterHisoricalAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        logger.debug("call => TwitterHisoricalAnalysis() Method Test Error => " + str(e))

    try:

        logger.debug("call => TwitterHistoricalAnalysisToDatabase() Method Test Starting... ")
        # TwitterHistoricalAnalysis() Method Test
        # create a stub (client)
        stub = grpc_services.TwitterHistoricalAnalysisStub(channel)

        # Setting the credentials up
        credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
                                                     consumer_secret=twitter_test_data.consumer_secret,
                                                     access_token=twitter_test_data.access_token,
                                                     token_secret=twitter_test_data.token_secret)
        # Setting the input message up
        message = rpc.TwitterInputMessage(
            credentials=credentials,
            languages=twitter_test_data.languages,
            query=twitter_test_data.query,
            product=twitter_test_data.product,
            environment=twitter_test_data.environment,
            from_date=twitter_test_data.fromDate,
            to_date=twitter_test_data.toDate,
            messages_per_request=twitter_test_data.messages_per_request,
            max_requests_limit=twitter_test_data.max_requests_limit,
            db_name=twitter_test_data.db_name)

        # make the call
        response = stub.HistoricalAnalysisToDatabase(message)
        logger.debug("call => TwitterHistoricalAnalysisToDatabase() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        logger.debug("call => TwitterHistoricalAnalysisToDatabase() Method Test Error => " + str(e))

    try:

        logger.debug("call => TwitterStreamAnalysis() Method Test Starting... ")
        print()
        # TwitterStreamAnalysis() Method Test
        # create a stub (client)
        stub = grpc_services.TwitterStreamAnalysisStub(channel)

        # Setting the credentials up
        credentials = rpc.TwitterCredentials(consumer_key=twitter_test_data.consumer_key,
                                                     consumer_secret=twitter_test_data.consumer_secret,
                                                     access_token=twitter_test_data.access_token,
                                                     token_secret=twitter_test_data.token_secret)
        # Setting the input message up
        message = rpc.TwitterInputMessage(
            credentials=credentials,
            languages=twitter_test_data.languages,
            query=twitter_test_data.query,
            time_limit=twitter_test_data.time_limit,
            msg_limit=twitter_test_data.msg_limit)

        # make the call
        response = stub.StreamAnalysis(message)
        logger.debug("call => TwitterStreamAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        logger.debug("call => TwitterStreamAnalysis() Method Test Error => " + str(e))
