import pathlib
import subprocess
import threading
import time
import sys
import glob
import argparse

from services import registry
from log import log_config

logger = log_config.getLogger('run_service.py')


def main():
    logger.debug('call => main()')
    parser = argparse.ArgumentParser(description="Run services")
    parser.add_argument("--no-daemon", action="store_false", dest="run_daemon", help="do not start the daemon")
    args = parser.parse_args()

    root_path = pathlib.Path(__file__).absolute().parent

    # All services modules go here
    service_modules = [
        'services.named_entity_recognition'
    ]

    # Call for all the services listed in service_modules
    start_all_services(root_path, service_modules, args.run_daemon)

    # Infinite loop to serve the services
    while True:
        try:
            time.sleep(1)
        except Exception as e:
            print(e)
            exit(0)


def start_all_services(cwd, service_modules, run_daemon):
    '''
    Loop through all service_modules and start them.
    For each one, an instance of Daemon 'snetd' is created.
    snetd will start with configs from 'snet_SERVICENAME_config.json'
    and will create a 'db_SERVICENAME.db' database file for each services.
    '''
    try:
        logger.debug('Starting start_all_services()')

        for i, service_module in enumerate(service_modules):
            service_name = service_module.split('.')[-1]
            print("Launching", service_module,"on ports", str(registry[service_name]))

            processThread = threading.Thread(target=start_service, args=(cwd, service_module, run_daemon))

            # Bind the thread with the main() to abort it when main() exits.
            processThread.daemon = True
            processThread.start()

        logger.debug('start_all_services() started')

    except Exception as e:
        print(e)
        return False

    return True


def start_service(cwd, service_module, run_daemon):
    '''
    Starts the python module of the services at the passed gRPC port and
    an instance of 'snetd' for the services.
    '''
    logger.debug('Starting start_service()')

    service_name = service_module.split('.')[-1]
    grpc_port = registry[service_name]['grpc']
    subprocess.Popen([sys.executable, '-m', service_module, '--grpc-port', str(grpc_port)],cwd=str(cwd))
    if run_daemon:
        for idx, config_file in enumerate(glob.glob("./config/*.json")):
            logger.debug("calling snetd")
            start_snetd(str(cwd), config_file)

    logger.debug('start_service() started')


def start_snetd(cwd, config_file=None):
    '''
    Starts the Daemon 'snetd' with:
    - Configurations from: config_file
    '''

    logger.debug('Starting start_snetd()')
    if config_file:
        cmd = ["snetd", "serve", "--config", str(config_file)]
        subprocess.Popen(cmd, cwd=str(cwd))
        logger.debug('start_snetd() started')
        return True
    logger.debug('No Daemon config file!')
    return False


if __name__ == "__main__":
    main()
