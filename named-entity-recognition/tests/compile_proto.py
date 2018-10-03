import path_setup
import pkg_resources
from grpc_tools.protoc import main as protoc
from pathlib import Path
import os


def compile_proto(entry_path, codegen_dir, proto_file=None):
    try:
        if not os.path.exists(codegen_dir):
            os.makedirs(codegen_dir)
        proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')
        protoc_args = [
            "protoc",
            "-I{}".format(entry_path),
            '-I{}'.format(proto_include),
            "--python_out={}".format(codegen_dir),
            "--grpc_python_out={}".format(codegen_dir)
        ]
        if proto_file:
            protoc_args.append(str(proto_file))
        else:
            protoc_args.extend([str(p) for p in entry_path.glob("**/*.proto")])

        if not protoc(protoc_args):
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False


path = Path("../services/service_spec")
success = compile_proto(path, path)
