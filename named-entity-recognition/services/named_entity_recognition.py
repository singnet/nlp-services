import sys
import grpc
import base64
import concurrent.futures as futures
from services.modules import entity_recognizer_mod
from services.service_spec import named_entity_recognition_rpc_pb2_grpc as grpc_bt_grpc
from services.service_spec.named_entity_recognition_rpc_pb2 import OutputMessage
from services import common
from log import log_config

logger = log_config.getLogger('named_entity_recognition.py')


class RecognizeMessageServicer(grpc_bt_grpc.RecognizeMessageServicer):
    """
    Create a class to be added to the gRPC server.
    """

    def __init__(self):
        # Just for debugging purpose.
        logger.debug("RecognizeMessageServicer created")
        self.recognizer = entity_recognizer_mod.SnetEntityRecognizer()

    def Recognize(self, request, context):
        """
        The method that will be exposed to the snet-cli call command.
        :param self:
        :param request: incoming data
        :param context: object that provides RPC-specific information (timeout, etc).
        :return:
        """

        # In our case, request is a InputMessage() object (from .proto file)
        # self.value = request.value
        self.value = request.value
        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        # Base64 decoding
        sentence = base64.b64decode(self.value).decode('utf-8')

        # Classifying sentences
        entities = self.recognizer.stanford_recognizer(sentence)

        # Building result list
        result_list = []

        for item in entities:
            start_index = sentence.find(item[0])
            end_index = start_index + len(item[0])
            result_list.append((item[0], item[1], 'Start span:', start_index, 'End span:', end_index))

        # Encoding result
        resultBase64 = base64.b64encode(str(result_list).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # logger.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


def serve(max_workers=10, port=7777):
    '''
    The gRPC serve function.

    Params:
    max_workers: pool of threads to execute calls asynchronously
    port: gRPC server port

    Add all your classes to the server here.
    (from generated .py files by protobuf compiler)
    '''
    logger.debug('call => serve(max_workers={}, port={})'.format(max_workers, port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_RecognizeMessageServicer_to_server(RecognizeMessageServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


# Runs the gRPC server to communicate with the Snet Daemon.
if __name__ == '__main__':
    logger.debug('call => __name__ == __main__')
    parser = common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    common.main_loop(serve, args)
