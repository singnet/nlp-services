import json
import os
import datetime
import sys
import base64
import grpc
import concurrent.futures as futures
from services.modules import consensus_mod, twitter_mod
from services.service_spec import sentiment_analysis_rpc_pb2_grpc as grpc_services
from services.service_spec.sentiment_analysis_rpc_pb2 import OutputMessage
from services import common
from log import log_config
from nltk.sentiment import SentimentIntensityAnalyzer

# Services Path
current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
service_root_path = os.path.abspath(os.path.join(parent_path, os.pardir))

logger = log_config.getLogger('sentiment_analysis.py')


class ShowMessageServicer(grpc_services.ShowMessageServicer):
    """ Create a class to be added to the gRPC server
    derived from the protobuf codes.
    """

    def __init__(self):
        logger.debug("call => ShowMessageServicer()")

    def Show(self, request, context):
        """ The method that will be exposed to the snet-cli call command.

        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        self.result.value = "Processed => " + self.value
        logger.debug('call => Show({})={}'.format(self.value, self.result.value))
        return self.result


class SentimentConsensusAnalysisServicer(grpc_services.SentimentConsensusAnalysisServicer):
    """ Create a class to be added to the gRPC server
    derived from the protobuf codes.
    """

    def __init__(self):
        logger.debug("call => SentimentConsensusAnalysisServicer()")

    def ConsensusAnalysis(self, request, context):
        """ The method that will be exposed to the snet-cli call command.

        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # Decode do string
        temp = base64.b64decode(self.value).decode('utf-8')
        # Convert in array
        tempArray = temp.split("\n")
        # Result of sentences
        stringResult = ''

        # Sentiment Analyser Instance
        analizer = SentimentIntensityAnalyzer()

        # Generating result
        for line in tempArray:
            if line is not None:
                if len(line) > 1:
                    stringResult += line
                    stringResult += '\n'
                    stringResult += str(analizer.polarity_scores(line))
                    stringResult += '\n\n'

        # Encoding result
        resultBase64 = base64.b64encode(str(stringResult).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        logger.debug('call => ConsensusAnalysis({})={}'.format(self.value, self.result.value))
        return self.result


class TwitterHistoricalAnalysisServicer(grpc_services.TwitterHistoricalAnalysisServicer):
    """ Create a class to be added to the gRPC server
    derived from the protobuf codes.
    """
    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => TwitterHistoricalAnalysisServicer()")
        self.reader = None
        self.db_name = None
        self.stringResult = ''
        self.resultBase64 = ''

    def twitter_reader_analysis(self, reader):
        """ Analyze twitter messages from reader
        :param reader:
        :return:
        """

        string_result = ''

        if len(reader.messages) > 0:
            analizer = SentimentIntensityAnalyzer()
            # Generating result
            for page in reader.messages:
                for item in page:
                    string_result += item['text']
                    string_result += '\n'
                    string_result += str(analizer.polarity_scores(item['text']))
                    string_result += '\n\n'

        return string_result

    def HistoricalAnalysis(self, request, context):
        """ The method that will be exposed to the snet-cli call command.

        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        try:
            # Setting up the Stream Manager
            self.reader = twitter_mod.TwitterApiReader(consumer_key=request.credentials.consumer_key,
                                                       consumer_secret=request.credentials.consumer_secret,
                                                       access_token=request.credentials.access_token,
                                                       token_secret=request.credentials.token_secret,
                                                       product=request.product,
                                                       environment=request.environment,
                                                       query=request.query,
                                                       messages_per_request=request.messages_per_request,
                                                       max_requests_limit=request.max_requests_limit,
                                                       msg_limit=request.msg_limit,
                                                       time_limit=request.time_limit,
                                                       from_date=request.from_date,
                                                       to_date=request.to_date,
                                                       db_name=request.db_name)

            # Start reading messages
            self.reader.read()

            # If the reader has captured messages then analyze them
            if len(self.reader.messages) > 0:
                # Analyze twitter messages from reader
                self.stringResult = self.twitter_reader_analysis(self.reader)
            else:
                self.stringResult = "Messages not found"

        except Exception as e:
            self.stringResult = "Error => " + str(e) + " at: " + str(datetime.datetime.now())
            logger.debug("call => HistoricalAnalysis() " + self.stringResult)

        finally:
            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => historicalAnalysis()={}'.format(self.result.value))
            return self.result


class TwitterStreamAnalysisServicer(grpc_services.TwitterStreamAnalysisServicer):
    """ Create a class to be added to the gRPC server
    derived from the protobuf codes.
    """

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("call => TwitterStreamAnalysisServicer()")
        self.manager = None
        self.status_error_code = None
        self.stringResult = ''
        self.resultBase64 = ''

    def twitter_manager_analysis(self, manager):

        sentences = manager.sentences()

        if len(sentences) > 0:
            analizer = SentimentIntensityAnalyzer()
            # Generating result
            for line in sentences:
                if line is not None:
                    if len(line) > 1:
                        self.stringResult += line
                        self.stringResult += '\n'
                        self.stringResult += str(analizer.polarity_scores(line))
                        self.stringResult += '\n\n'
        else:
            self.status_error_code = str(self.manager.status_error_code())

        return self.stringResult

    def StreamAnalysis(self, request, context):
        """ The method that will be exposed to the snet-cli call command.

        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        try:

            # Setting up the Stream Manager
            self.manager = twitter_mod.SnetStreamManager(consumer_key=request.credentials.consumer_key,
                                                         consumer_secret=request.credentials.consumer_secret,
                                                         access_token=request.credentials.access_token,
                                                         token_secret=request.credentials.token_secret,
                                                         msg_limit=request.time_limit,
                                                         time_limit=request.msg_limit)

            # Start filtering on twitter
            self.manager.filter(languages=request.languages, query=request.query)

            # Generating analysis result
            self.twitter_manager_analysis(self.manager)

        except Exception as e:

            if self.status_error_code:
                self.stringResult = "Error => status code => " + self.status_error_code \
                                    + " at: " + str(datetime.datetime.now())
                logger.error('Error description => ' + self.stringResult)

        finally:
            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => StreamAnalysis()={}'.format(self.result.value))
            return self.result


def serve(max_workers=10, port=7777):
    """ The gRPC serve function.

    Add all your classes to the server here.
    (from generated .py files by protobuf compiler)

    :param max_workers: pool of threads to execute calls asynchronously
    :param port: gRPC server port
    :return:
    """

    logger.debug('call => serve(max_workers={}, port={})'.format(max_workers, port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_services.add_ShowMessageServicer_to_server(ShowMessageServicer(), server)
    grpc_services.add_SentimentConsensusAnalysisServicer_to_server(SentimentConsensusAnalysisServicer(), server)
    grpc_services.add_TwitterHistoricalAnalysisServicer_to_server(TwitterHistoricalAnalysisServicer(), server)
    grpc_services.add_TwitterStreamAnalysisServicer_to_server(TwitterStreamAnalysisServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    """ Runs the gRPC server to communicate with the Snet Daemon.
    """
    logger.debug('call => __name__ == __main__')
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
