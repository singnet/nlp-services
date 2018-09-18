import grpc

# import the generated classes
from services.service_spec import named_entity_recognition_rpc_pb2_grpc as grpc_bt_grpc
from services.service_spec import named_entity_recognition_rpc_pb2 as grpc_bt_pb2
from services import registry
from test_data import b64_sentences
from log import log_config

logger = log_config.getLogger('test_service.py')

if __name__ == '__main__':

    try:
        logger.debug('call => __name == __main__')

        logger.debug("call => Creating channel() Starting... ")
        print()
        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['named_entity_recognition']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

    except Exception as e:
        logger.debug("Error found Creating Channel => " + e)

    try:
        # ShowMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.ShowMessageStub(channel)
        # create a valid request message
        test_text = "message received from God"
        message = grpc_bt_pb2.InputMessage(value=test_text)
        # make the call
        response = stub.show(message)
        logger.debug("call => ShowMessage() Method Test Passed => " + response.value)
        print()

    except Exception as e:
        logger.debug("Error found => " + e)

    try:
        logger.debug("call => RecognizeMessage() Method Test Starting... ")
        print()
        # RecognizeMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.RecognizeMessageStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.recognize(message)
        logger.debug("call => RecognizeMessage() Method Test Passed => " + response.value)
        print()

    except Exception as e:
        logger.debug(e)
