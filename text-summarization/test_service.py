import sys
import grpc

# import the generated classes
import services.service_spec.summary_pb2_grpc as grpc_bt_grpc
import services.service_spec.summary_pb2 as grpc_bt_pb2

from services import registry

with open("example_article.txt", "r") as f:
    TEST_TEXT = f.read()

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        endpoint = input("Endpoint (localhost:{}): ".format(registry["summary_server"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["summary_server"]["grpc"])

        grpc_method = input("Method (summary): ") if not test_flag else "summary"
        article_content = input("Text: ") if not test_flag else TEST_TEXT

        # open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))
        request = grpc_bt_pb2.Request(article_content=article_content)
        stub = grpc_bt_grpc.TextSummaryStub(channel)

        if grpc_method == "summary":
            response = stub.summary(request)
            print("Article Summary:", response.article_summary)
            if len(response.article_summary) < 1:
                exit(1)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
