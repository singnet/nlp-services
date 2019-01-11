import sys
import time
import logging
import traceback

import grpc
import concurrent.futures as futures

import service.common
from service.language_understanding import LanguageUnderstanding

# Importing the generated codes from buildproto.sh
import service.service_spec.language_understanding_pb2_grpc as grpc_bt_grpc
from service.service_spec.language_understanding_pb2 import Output

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("language_understanding_service")

GPU_DEVICE_BUSY = False
GPU_QUEUE = []
GPU_QUEUE_ID = -1


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class LanguageUnderstandingServicer(grpc_bt_grpc.LanguageUnderstandingServicer):
    def __init__(self):
        self.train_ctf_url = ""
        self.test_ctf_url = ""
        self.query_wl_url = ""
        self.slots_wl_url = ""
        self.intent_wl_url = ""
        self.sentences_url = ""

        self.vocab_size = 0
        self.num_labels = 0
        self.num_intents = 0

        self.response = None

        log.debug("LanguageUnderstandingServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def slot_tagging(self, request, context):

        gpu_queue_id = get_gpu_queue_id()
        try:
            # Wait to use GPU (max: 1h)
            count = 0
            while GPU_DEVICE_BUSY or GPU_QUEUE[0] != gpu_queue_id:
                time.sleep(1)
                if count % 60 == 0:
                    log.debug("[Client: {}] GPU is being used by [{}], waiting...".format(gpu_queue_id, GPU_QUEUE[0]))
                count += 1
                if count > 60 * 60:
                    self.response = Output()
                    self.response.last_sax_word = "GPU Busy"
                    self.response.forecast_sax_letter = "GPU Busy"
                    self.response.position_in_sax_interval = -1
                    return self.response

            # Lock GPU usage
            acquire_gpu(gpu_queue_id)

            # In our case, request is an Input() object (from .proto file)
            self.train_ctf_url = request.train_ctf_url
            self.test_ctf_url = request.test_ctf_url
            self.query_wl_url = request.query_wl_url
            self.slots_wl_url = request.slots_wl_url
            self.intent_wl_url = request.intent_wl_url

            self.vocab_size = request.vocab_size
            self.num_labels = request.num_labels
            self.num_intents = request.num_intents

            self.sentences_url = request.sentences_url

            mst = LanguageUnderstanding(
                self.train_ctf_url,
                self.test_ctf_url,
                self.query_wl_url,
                self.slots_wl_url,
                self.intent_wl_url,
                self.vocab_size,
                self.num_labels,
                self.num_intents,
                self.sentences_url
            )

            tmp_response = mst.language_understanding()

            # To respond we need to create an Output() object (from .proto file)
            self.response = Output()
            self.response.model_url = str(tmp_response["model_url"]).encode("utf-8")
            self.response.output_url = str(tmp_response["output_url"]).encode("utf-8")

            log.debug("slot_tagging({})={},{}".format(
                self.sentences_url,
                self.response.output_url,
                self.response.model_url)
            )

            # Unlock GPU usage
            release_gpu(gpu_queue_id)

            return self.response

        except Exception as e:
            if gpu_queue_id == GPU_QUEUE[0]:
                release_gpu(gpu_queue_id)
            else:
                remove_from_queue(gpu_queue_id)
            traceback.print_exc()
            log.error(e)
            self.response = Output()
            self.response.model_url = "Fail"
            self.response.output_url = "Fail"
            return self.response

    # Intent classification
    def intent(self, request, context):

        gpu_queue_id = get_gpu_queue_id()
        try:
            # Wait to use GPU (max: 1h)
            count = 0
            while GPU_DEVICE_BUSY or GPU_QUEUE[0] != gpu_queue_id:
                time.sleep(1)
                if count % 60 == 0:
                    log.debug(
                        "[Client: {}] GPU is being used by [{}], waiting...".format(gpu_queue_id, GPU_QUEUE[0]))
                count += 1
                if count > 60 * 60:
                    self.response = Output()
                    self.response.last_sax_word = "GPU Busy"
                    self.response.forecast_sax_letter = "GPU Busy"
                    self.response.position_in_sax_interval = -1
                    return self.response

            # Lock GPU usage
            acquire_gpu(gpu_queue_id)

            # In our case, request is an Input() object (from .proto file)
            self.train_ctf_url = request.train_ctf_url
            self.test_ctf_url = request.test_ctf_url
            self.query_wl_url = request.query_wl_url
            self.slots_wl_url = request.slots_wl_url
            self.intent_wl_url = request.intent_wl_url

            self.vocab_size = request.vocab_size
            self.num_labels = request.num_labels
            self.num_intents = request.num_intents

            self.sentences_url = request.sentences_url

            mst = LanguageUnderstanding(
                self.train_ctf_url,
                self.test_ctf_url,
                self.query_wl_url,
                self.slots_wl_url,
                self.intent_wl_url,
                self.vocab_size,
                self.num_labels,
                self.num_intents,
                self.sentences_url
            )

            tmp_response = mst.language_understanding(intent_model=True)

            # To respond we need to create a Output() object (from .proto file)
            self.response = Output()
            self.response.model_url = str(tmp_response["model_url"]).encode("utf-8")
            self.response.output_url = str(tmp_response["output_url"]).encode("utf-8")

            log.debug("intent({})={},{}".format(
                self.sentences_url,
                self.response.output_url,
                self.response.model_url)
            )

            # Unlock GPU usage
            release_gpu(gpu_queue_id)

            return self.response

        except Exception as e:
            if gpu_queue_id == GPU_QUEUE[0]:
                release_gpu(gpu_queue_id)
            else:
                remove_from_queue(gpu_queue_id)
            traceback.print_exc()
            log.error(e)
            self.response = Output()
            self.response.model_url = "Fail"
            self.response.output_url = "Fail"
            return self.response


def get_gpu_queue_id():
    global GPU_QUEUE
    global GPU_QUEUE_ID
    GPU_QUEUE_ID += 1
    GPU_QUEUE.append(GPU_QUEUE_ID)
    log.debug("[Client: {}]                  GPU_QUEUE     : {}".format(GPU_QUEUE_ID, GPU_QUEUE))
    return GPU_QUEUE_ID


def remove_from_queue(gpu_queue_id):
    global GPU_QUEUE
    GPU_QUEUE.remove(gpu_queue_id)


def acquire_gpu(gpu_queue_id):
    global GPU_DEVICE_BUSY
    global GPU_QUEUE
    GPU_DEVICE_BUSY = True
    log.debug("[Client: {}] Acquiring GPU (GPU_DEVICE_BUSY): {}".format(gpu_queue_id, GPU_DEVICE_BUSY))


def release_gpu(gpu_queue_id):
    global GPU_DEVICE_BUSY
    remove_from_queue(gpu_queue_id)
    GPU_DEVICE_BUSY = False
    log.debug("[Client: {}] Releasing GPU (GPU_DEVICE_BUSY): {}".format(gpu_queue_id, GPU_DEVICE_BUSY))
    log.debug("[Client: {}]                  GPU_QUEUE     : {}".format(gpu_queue_id, GPU_QUEUE))


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_LanguageUnderstandingServicer_to_server(LanguageUnderstandingServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = service.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    service.common.main_loop(serve, args)