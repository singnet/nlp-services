import pathlib
import subprocess
import signal
import time
import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(prog="run-snet-services")
    parser.add_argument("--daemon-config-path", help="Path to daemon configuration file", required=False)
    args = parser.parse_args(sys.argv[1:])
    
    root_path = pathlib.Path(__file__).absolute().parent
    all_p = [start_snetd(root_path, args.daemon_config_path), start_service(root_path)]
    
    # Continuous checking all subprocess
    while True:
        for p in all_p:
            p.poll()
            if p.returncode and p.returncode != 0:
                kill_and_exit(all_p)
        time.sleep(1)


def start_snetd(cwd, daemon_config_path=None):
    cmd = ["snetd", "serve"]
    if daemon_config_path is not None:
        cmd.extend(["--config", daemon_config_path])
    return subprocess.Popen(cmd, cwd=cwd)


def start_service(cwd):
    return subprocess.Popen(["python3.6", "-m", "services.summary_server"], cwd=cwd)


def kill_and_exit(all_p):
    """
    Kills main, service and daemon's processes if one fails.
    """
    for p in all_p:
        try:
            os.kill(p.pid, signal.SIGTERM)
        except Exception as e:
            print(e)
    exit(1)


if __name__ == "__main__":
    main()
