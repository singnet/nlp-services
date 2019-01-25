import os
import sys
import base64
import grpc
import concurrent.futures as futures
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


class SentimentAnalysisServicer(grpc_services.SentimentAnalysisServicer):
    """ Create a class to be added to the gRPC server
    derived from the protobuf codes.
    """

    def __init__(self):
        logger.debug("call => SentimentAnalysisServicer()")

    def Analyze(self, request, context):
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
        logger.debug('call => Analyze({})={}'.format(self.value, self.result.value))
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
    grpc_services.add_SentimentAnalysisServicer_to_server(SentimentAnalysisServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    """ Runs the gRPC server to communicate with the Snet Daemon.
    """
    logger.debug('call => __name__ == __main__')
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
