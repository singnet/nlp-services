import grpc

# import the generated classes
import services.model.sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
import services.model.sentiment_analysis_rpc_pb2 as grpc_bt_pb2
from tests_data import b64_sentences
from services import registry

if __name__ == '__main__':

    try:
        print("ShowMessage() Method Test Starting... ")
        print()
        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

        # ShowMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.ShowMessageStub(channel)
        # create a valid request message
        test_text = "RODANDO TESTES..."
        message = grpc_bt_pb2.InputMessage(value=test_text)
        # make the call
        response = stub.show(message)
        print("ShowMessage() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:
        print("SentimentIntensityAnalysis() Method Test Starting... ")
        print()
        # SentimentIntensityAnalysis() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.SentimentIntensityAnalysisStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.intensivityAnalysis(message)
        print("SentimentIntensityAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:

        print("SentimentComplexAnalysis() Method Test Starting... ")
        print()
        # SentimentComplexAnalysis() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.SentimentComplexAnalysisStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.complexAnalysis(message)
        print("SentimentComplexAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:

        # print("CustomCorpusAnalysis() Method Test Starting... ")
        # print()
        # # CustomCorpusAnalysis() Method Test
        # # create a stub (client)
        # stub = grpc_bt_grpc.CustomCorpusAnalysisStub(channel)
        # # create a valid request message
        # test_text = "RODANDO TESTES..."
        # message = grpc_bt_pb2.InputMessage(value=test_text)
        # # make the call
        # response = stub.show(message)
        # print("CustomCorpusAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)

    try:

        # print("TwitterAnalysis() Method Test Starting... ")
        # print()
        # TwitterAnalysis() Method Test
        # create a stub (client)
        # stub = grpc_bt_grpc.TwitterAnalysisStub(channel)
        # create a valid request message
        # languages = 'pt'
        # sentences = 'Lula presidente'
        # message = grpc_bt_pb2.TwitterInputMessage(languages=languages, sentences=sentences)
        # make the call
        # response = stub.twitterAnalysis(message)
        # print("TwitterAnalysis() Method Test Passed => " + response.value)
        print()

    except KeyError as e:
        print(e)
