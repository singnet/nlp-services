import datetime
import sys
import base64
import grpc
import concurrent.futures as futures
from nltk.sentiment import SentimentIntensityAnalyzer
from services.modules import consensus_mod, twitter_mod
from services.service_spec import sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
from services.service_spec.sentiment_analysis_rpc_pb2 import OutputMessage
from services import common
from log import log_config

logger = log_config.getLogger('sentiment_analysis.py')


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ShowMessageServicer(grpc_bt_grpc.ShowMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => ShowMessageServicer()")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def show(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        self.result.value = "Processed => " + self.value
        logger.debug('call => show({})={}'.format(self.value, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class SentimentConsensusAnalysisServicer(grpc_bt_grpc.SentimentConsensusAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => SentimentConsensusAnalysisServicer()")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def consensusAnalysis(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        text = base64.b64decode(self.value)
        # Decode do string
        temp = text.decode('utf-8')
        # Convert in array
        tempArray = temp.split("\n")
        # Result of sentences
        stringResult = ''

        # Generating result
        for line in tempArray:
            if line is not None:
                if len(line) > 1:
                    stringResult += line
                    stringResult += '\n'
                    stringResult += str(consensus_mod.sentiment(line))
                    stringResult += '\n\n'

        # Encoding result
        resultBase64 = base64.b64encode(str(stringResult).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        logger.debug('call => consensusAnalysis({})={}'.format(self.value, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class TwitterHistoricalAnalysisServicer(grpc_bt_grpc.TwitterHistoricalAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => TwitterHistoricalAnalysisServicer()")
        self.reader = None
        self.stringResult = ''
        self.resultBase64 = ''

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def historicalAnalysis(self, request, context):
        try:
            # Setting up the Stream Manager
            self.reader = twitter_mod.TwitterApiReader(consumer_key=request.credentials.consumer_key,
                                                       consumer_secret=request.credentials.consumer_secret,
                                                       access_token=request.credentials.access_token,
                                                       token_secret=request.credentials.token_secret)
            # Twitter query parameters config
            product = request.product
            environment = request.environment
            url = "https://api.twitter.com/1.1/tweets/search/" + product + "/" + environment + '.json'
            params = {"query": request.keywords, "maxResults": request.max_results, "fromDate": request.from_date,
                      "toDate": request.to_date}

            # Start searching on twitter
            self.reader.read(url=url, params=params)
            messages = self.reader.messages()

            if len(messages) > 0:
                # Generating result
                for line in messages:
                    if line is not None:
                        if len(line) > 1:
                            self.stringResult += line
                            self.stringResult += '\n'
                            self.stringResult += str(consensus_mod.sentiment(line))
                            self.stringResult += '\n\n'

        except Exception as e:
            logger.debug('call => historicalAnalysis() error => ' + str(e))
            if self.reader.error_message is not '':
                self.stringResult = " status => " + self.reader.error_message + " at: " + str(datetime.datetime.now())
                logger.error('Error description => ' + self.stringResult)

        finally:
            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => historicalAnalysis()={}'.format(self.result.value))
            return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class TwitterStreamAnalysisServicer(grpc_bt_grpc.TwitterStreamAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => TwitterStreamAnalysisServicer()")
        self.manager = None
        self.status_error_code = None
        self.stringResult = ''
        self.resultBase64 = ''

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def streamAnalysis(self, request, context):
        try:

            # Setting up the Stream Manager
            self.manager = twitter_mod.SnetStreamManager(consumer_key=request.credentials.consumer_key,
                                                         consumer_secret=request.credentials.consumer_secret,
                                                         access_token=request.credentials.access_token,
                                                         token_secret=request.credentials.token_secret,
                                                         msg_limit=request.time_limit,
                                                         time_limit=request.msg_limit)

            # Start filtering on twitter
            self.manager.filter(languages=request.languages, keywords=request.keywords)

            sentences = self.manager.sentences()

            if len(sentences) > 0:
                # Generating result
                for line in sentences:
                    if line is not None:
                        if len(line) > 1:
                            self.stringResult += line
                            self.stringResult += '\n'
                            self.stringResult += str(consensus_mod.sentiment(line))
                            self.stringResult += '\n\n'
            else:
                self.status_error_code = str(self.manager.status_error_code())

        except Exception as e:
            if self.status_error_code:
                self.stringResult = " status error code => " + self.status_error_code + " at: " + str(datetime.datetime.now())
                logger.error('Error description => ' + self.stringResult)

        finally:

            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => streamAnalysis()={}'.format(self.result.value))
            return self.result


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    logger.debug('call => serve(max_workers={}, port={})'.format(max_workers, port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_ShowMessageServicer_to_server(ShowMessageServicer(), server)
    grpc_bt_grpc.add_SentimentConsensusAnalysisServicer_to_server(SentimentConsensusAnalysisServicer(), server)
    grpc_bt_grpc.add_TwitterHistoricalAnalysisServicer_to_server(TwitterHistoricalAnalysisServicer(), server)
    grpc_bt_grpc.add_TwitterStreamAnalysisServicer_to_server(TwitterStreamAnalysisServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    logger.debug('call => __name__ == __main__')
    '''
    Runs the gRPC server to communicate with the Snet Daemon.
    '''
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
