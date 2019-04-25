import sys
import grpc
import json
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
        # decoded_senteces = base64.b64decode(self.value).decode('utf-8')

        # Convert in json array
        sentence_list = json.loads(self.value)

        # Result list
        result_list = []

        for sentence_item in sentence_list:
            # Classifying sentences
            entities = self.recognizer.stanford_recognizer(sentence_item["sentence"])

            # Building entity list
            entity_list = []

            for entity_item in entities:
                start_index = sentence_item["sentence"].find(entity_item[0])
                end_index = start_index + len(entity_item[0])
                entity_list.append({
                    "name": entity_item[0],
                    "type": entity_item[1],
                    "start_span": start_index,
                    "end_span": end_index
                })

            result_list.append({"id": sentence_item["id"], "entities": entity_list})

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = json.dumps(result_list)
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
