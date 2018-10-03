import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
sys.path.append(parent_path)
sys.path.append(parent_path + '/services/service_spec')

# spec_path = parent_path + '/services/service_spec'
# print(str(sys.path))
# sys.path.remove(parent_path)
# sys.path.remove(spec_path)
# print(str(sys.path))


def clean_paths():
    sys.path.remove(parent_path)
    sys.path.remove(parent_path + '/services/service_spec')