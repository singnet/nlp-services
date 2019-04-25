import path_setup
import grpc
from services.service_spec import sentiment_analysis_rpc_pb2_grpc as grpc_services
from services.service_spec import sentiment_analysis_rpc_pb2 as rpc
from test_data import test_sentences
from services import registry
from log import log_config

logger = log_config.getLogger('test_service.py', test=True)
channel = None

if __name__ == '__main__':

    try:
        logger.debug('call => __name == __main__')
        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

    except KeyError as e:
        print(e)

    try:

        logger.debug("call => SentimentAnalysis() Service Test Starting... ")
        # SentimentAnalysis() Method Test
        # create a stub (client)
        stub = grpc_services.SentimentAnalysisStub(channel)
        # create a valid request message
        test_data = test_sentences.senteces()
        message = rpc.InputMessage(value=test_data)
        # make the call
        response = stub.Analyze(message)
        logger.debug("call => Analyze() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

path_setup.clean_paths()