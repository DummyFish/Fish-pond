from multiprocessing import Process
from services.ssh.ssh import SSH
from services.smtp import smtp
from services.ftp import ftp
from services.telnet import telnet
from services.rdp import rdp
from services.redis import redis
from services.pop3 import pop3
from services.tftp import tftp


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
        smtp_process = Process(target=smtp.SMTP, args=(host, smtp_port, log_filepath, "smtp"))
        smtp_process.start()

    ftp_states = config.get('ftp', 'status', raw=True, fallback="0")
    if ftp_states == "1":
        print("service ftp start")
        ftp_port = config.get('ftp', 'port', raw=True, fallback="21")
        ftp_process = Process(target=ftp.FTP, args=(host, ftp_port, log_filepath, "ftp"))
        ftp_process.start()

    telnet_states = config.get('telnet', 'status', raw=True, fallback="0")
    if telnet_states == "1":
        print("service telnet start")
        telnet_port = config.get('telnet', 'port', raw=True, fallback="23")
        telnet_process = Process(target=telnet.Telnet, args=(host, telnet_port, log_filepath, "telnet"))
        telnet_process.start()


    rdp_states = config.get('rdp', 'status', raw=True, fallback="0")
    if rdp_states == "1":
        print("service rdp start")
        rdp_port = config.get('rdp', 'port', raw=True, fallback="3389")
        # RDP(host, rdp_port, log_filepath, "rdp")
        rdp_process = Process(target=rdp.RDP, args=(host, rdp_port, log_filepath, "rdp"))
        rdp_process.start()

    redis_states = config.get('redis', 'status', raw=True, fallback="0")
    if redis_states == "1":
        print("service redis start")
        redis_port = config.get('redis', 'port', raw=True, fallback="6379")
        # Redis(host, redis_port, log_filepath, "redis")
        redis_process = Process(target=redis.Redis, args=(host, redis_port, log_filepath, "redis"))
        redis_process.start()
    
    pop3_states = config.get('pop3', 'status', raw=True, fallback="0")
    if pop3_states == "1":
        print("service pop3 start")
        pop3_port = config.get('pop3', 'port', raw=True, fallback="995")
        # POP3(host, redis_port, log_filepath, "redis")
        pop3_process = Process(target=pop3.POP3, args=(host, pop3_port, log_filepath, "pop3"))
        pop3_process.start()

    tftp_states = config.get('tftp', 'status', raw=True, fallback="0")
    if tftp_states == "1":
        print("service tftp start")
        tftp_port = config.get('tftp', 'port', raw=True, fallback="69")
        # tftp(host, redis_port, log_filepath, "tftp")
        tftp_process = Process(target=tftp.TFTP, args=(host, tftp_port, log_filepath, "tftp"))
        tftp_process.start()

    # other service
    print("other")
