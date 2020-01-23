import sys
import grpc

# import the generated classes
import services.service_spec.translate_pb2_grpc as grpc_bt_grpc
import services.service_spec.translate_pb2 as grpc_bt_pb2

from services import registry

with open("example_de_article.txt", "r") as f:
    TEST_TEXT = f.read()

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        endpoint = input("Endpoint (localhost:{}): ".format(registry["translate_server"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["translate_server"]["grpc"])

        grpc_method = input("Method (translate): ") if not test_flag else "translate"
        text_content = input("Text: ") if not test_flag else TEST_TEXT

        # open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))
        request = grpc_bt_pb2.Request(
            text=text_content,
            source_language="de",
            target_language="en"
        )
        stub = grpc_bt_grpc.TranslationStub(channel)

        if grpc_method == "translate":
            response = stub.translate(request)
            print("Translation:", response.translation)
            if len(response.translation) < 1:
                exit(1)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
