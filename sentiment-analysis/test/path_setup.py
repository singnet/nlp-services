import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
sys.path.append(parent_path)
sys.path.append(parent_path + '/services/service_spec')


def clean_paths():
    sys.path.remove(parent_path)
    sys.path.remove(parent_path + '/services/service_spec')