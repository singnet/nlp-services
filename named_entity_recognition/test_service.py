import grpc

# import the generated classes
from services.model import named_entity_recognition_rpc_pb2_grpc as grpc_bt_grpc
from services.model import named_entity_recognition_rpc_pb2 as grpc_bt_pb2
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
        logger.debug("call => NltkClassifierMessage() Method Test Starting... ")
        print()
        # NltkClassifierMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.NltkClassifierMessageStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.nltk_classify(message)
        logger.debug("call => NltkClassifierMessage() Method Test Passed => " + response.value)
        print()

    except Exception as e:
        logger.debug(e)

    try:
        logger.debug("call => StanfordClassifierMessage() Method Test Starting... ")
        print()
        # StanfordClassifierMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.StanfordClassifierMessageStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.stanford_classify(message)
        logger.debug("call => StanfordClassifierMessage() Method Test Passed => " + response.value)
        print()

    except Exception as e:
        logger.debug(e)
