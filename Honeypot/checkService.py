from multiprocessing import Process
from Honeypot.services.ssh.ssh import SSH


def check(config):
    host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
    log_filepath = config.get('default', 'logfile', raw=True, fallback="./logfile.log")

    print("service started, check which service is started:")
    ssh_states = config.get('ssh', 'status', raw=True, fallback="0")
    if ssh_states == "1":
        print("service ssh start")
        ssh_port = config.get('ssh', 'port', raw=True, fallback="22")

        # SSH(host, ssh_port, log_filepath, "ssh")
        ssh_process = Process(target=SSH, args=(host, ssh_port, log_filepath, "ssh"))
        ssh_process.start()

    # other service
    print("other")
