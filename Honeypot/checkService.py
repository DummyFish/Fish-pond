from multiprocessing import Process
from services.ssh.ssh import SSH
from services.smtp.smtp import SMTP


def check(config):
    host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
    log_filepath = config.get('default', 'logfile', raw=True, fallback="./logfile.log")

    print("service started, check which service is started:")
    ssh_states = config.get('ssh', 'status', raw=True, fallback="0")
    if ssh_states == "1":
        print("service ssh start")
        ssh_port = config.get('ssh', 'port', raw=True, fallback="22")
        host_key = config.get('ssh', 'service_key', raw=True, fallback="../server.key")
        # SSH(host, ssh_port, log_filepath, "ssh")
        ssh_process = Process(target=SSH, args=(host, ssh_port, log_filepath, host_key, "ssh"))
        ssh_process.start()

    smtp_states = config.get('smtp', 'status', raw=True, fallback="0")
    if smtp_states == "1":
        print("service redis start")
        smtp_port = config.get('smtp', 'port', raw=True, fallback="2525")
        # SMTP(host, smtp_port, log_filepath, "smtp")
        smtp_process = Process(target=SMTP, args=(host, smtp_port, log_filepath, "smtp"))
        smtp_process.start()

    # other service
    print("other")
