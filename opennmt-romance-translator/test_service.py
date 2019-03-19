import sys
import grpc
import traceback

# import the generated classes
import service.service_spec.romance_translator_pb2_grpc as grpc_bt_grpc
import service.service_spec.romance_translator_pb2 as grpc_bt_pb2

from service import registry

if __name__ == "__main__":

    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True

        # Service ONE - Arithmetic
        endpoint = input("Endpoint (localhost:{}): ".format(registry["romance_translator_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(registry["romance_translator_service"]["grpc"])

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))

        default = "translate"
        grpc_method = input("Method (translate): ") if not test_flag else default
        if grpc_method == "":
            grpc_method = default

        default = "pt"
        source_lang = input("Source Language (pt): ") if not test_flag else default
        if source_lang == "":
            source_lang = default

        default = "it"
        target_lang = input("Target Language (it): ") if not test_flag else default
        if target_lang == "":
            target_lang = default

        default = "http://54.203.198.53:7000/Translation/OpenNMT/Romance/input_sentences.txt"
        sentences_url = input("Sentences URL (Example URL): ") if not test_flag else default
        if sentences_url == "":
            sentences_url = default

        stub = grpc_bt_grpc.RomanceTranslatorStub(channel)

        request = grpc_bt_pb2.Input(
            source_lang=source_lang,
            target_lang=target_lang,
            sentences_url=sentences_url
        )

        if grpc_method == "translate":
            response = stub.translate(request)
            print("\nresponse:")
            print("translation:")
            # To proper print UTF-8 without setting console's encoding
            sys.stdout.buffer.write(response.translation.encode("utf-8"))
            if "Fail" in response.translation:
                exit(1)
        else:
            print("Invalid method!")
            exit(1)

    except Exception as e:
        print(e)
        traceback.print_exc()
        exit(1)
