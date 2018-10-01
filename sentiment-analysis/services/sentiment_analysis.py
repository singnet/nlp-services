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
from services.modules import recognizer_mod
# TODO remove the line below
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

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
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
                                                       msg_limit=0,
                                                       time_limit=0,
                                                       max_requests_limit=0,
                                                       db_name=None)
            # Twitter query parameters config
            product = request.product
            environment = request.environment
            url = "https://api.twitter.com/1.1/tweets/search/" + product + "/" + environment + '.json'
            params = {"query": request.query, "maxResults": request.messages_per_request, "fromDate": request.from_date,
                      "toDate": request.to_date}

            # Start searching on twitter
            self.reader.read(url=url, params=params)

            if len(self.reader.messages) > 0:
                # Generating result
                for page in self.reader.messages:
                    for item in page:
                        self.stringResult += item['text']
                        self.stringResult += '\n'
                        self.stringResult += str(consensus_mod.sentiment(item['text']))
                        self.stringResult += '\n\n'

        except Exception as e:
            self.stringResult = " status => " + str(e) + " at: " + str(datetime.datetime.now())
            logger.debug('call => HistoricalAnalysisToDatabase() Error description => ' + self.stringResult)

        finally:
            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => historicalAnalysis()={}'.format(self.result.value))
            return self.result

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def HistoricalAnalysisToDatabase(self, request, context):
        """ The method that will be exposed to the snet-cli call command.

        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        try:

            self.recognizer = recognizer_mod.SnetRecognizer()

            self.db_name = 'twitter_messages'

            # Setting up the Stream Manager
            self.reader = twitter_mod.TwitterApiReader(consumer_key=request.credentials.consumer_key,
                                                       consumer_secret=request.credentials.consumer_secret,
                                                       access_token=request.credentials.access_token,
                                                       token_secret=request.credentials.token_secret,
                                                       msg_limit=request.msg_limit,
                                                       time_limit=request.time_limit,
                                                       max_requests_limit=request.max_requests_limit,
                                                       db_name=request.db_name)
            # Twitter query parameters config
            product = request.product
            environment = request.environment
            url = "https://api.twitter.com/1.1/tweets/search/" + product + "/" + environment + '.json'
            params = {"query": request.query, "maxResults": request.messages_per_request, "fromDate": request.from_date,
                      "toDate": request.to_date}

            # Start searching on twitter
            self.reader.read(url, params)
            # t1 = threading.Thread(target=self.reader.read, args=(url, params), daemon=True)
            # t1.start()

            # TODO working in progress
            # logger.debug("Start listening database")
            # while self.reader.reading:
            # with sqlite3.connect(self.db_name) as conn:
            #     cur = conn.cursor()
            #     cur.execute("select * from messages")
            #     rows = cur.fetchall()
            #     self.reader.messages = cur.fetchall()

            if len(self.reader.messages) > 0:
                analizer = SentimentIntensityAnalyzer()
                # if request.db_name:
                # Writing on txt file
                with open(request.db_name+'.txt', 'w') as filehandle:

                    # Reading all page of messages
                    for page in self.reader.messages:
                        # Reading page items
                        for item in page:
                            print("Processing entities...")
                            # Extracting entities
                            sentence_entities = self.recognizer.stanford_recognizer(item['text'])

                            print("Processing sentiment analysis...")
                            # Sentiment Analysis
                            # temp_sentiment_analysis = consensus_mod.sentiment(item['text'])
                            temp_sentiment_analysis = analizer.polarity_scores(item['text'])

                            # Writing output file
                            for entity in sentence_entities:
                                print("writting into txt file...")
                                # Twitter id
                                filehandle.write(str(item['id']) + ';')

                                # Entity
                                filehandle.write(str(entity[0]) + ';')

                                # Entity type
                                filehandle.write(str(entity[1]) + ';')

                                # Set Sentiment Analysis
                                filehandle.write(str(temp_sentiment_analysis))
                                filehandle.write('\n')
                self.stringResult = "Data generated successfully"

            else:
                self.stringResult = "Messages not found"

        except Exception as e:
            self.stringResult = " status => " + str(e) + " at: " + str(datetime.datetime.now())
            logger.debug('call => HistoricalAnalysisToDatabase() Error description => ' + self.stringResult)

        finally:
            # Encoding result
            self.resultBase64 = base64.b64encode(str(self.stringResult).encode('utf-8'))
            # To respond we need to create a OutputMessage() object (from .proto file)
            self.result = OutputMessage()
            self.result.value = self.resultBase64
            logger.debug('call => HistoricalAnalysisToDatabase()={}'.format(self.result.value))
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
                self.stringResult = " status error code => " + self.status_error_code + " at: " + str(
                    datetime.datetime.now())
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
