import configparser
import queue
from multiprocessing import Process
from time import sleep
from .services.smtp.smtp import SMTP
from .services.ssh.ssh import SSH
from .services.ftp.ftp import FTP
from .services.telnet.telnet import Telnet
from .services.rdp.rdp import RDP
from .services.redis.redis import Redis
from .services.pop3.pop3 import POP3
from .services.tftp.tftp import TFTP
from .modify_config import get_config
import multiprocessing
import sqlite3


class NormalException(BaseException):
    pass


def create_db():
    database = sqlite3.connect('../logger.db')
    data = database.cursor()
    cursor = data.execute("CREATE TABLE IF NOT EXISTS FishPond(id integer primary key NOT NULL, \
                          exetime Timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL, service varchar(64),types varchar(64), \
                          ip varchar(64), username varchar(64), password varchar(64), command varchar(1024))")
    return database


def send_to_sql(database, result):
    sql = ''' INSERT INTO FishPond(exetime,service,types,ip,username,password,command)
                  VALUES(?,?,?,?,?,?,?) '''
    time = result['time']
    service = result['service']
    datatype = result['type']
    ip = result['ip']
    username = result['username']
    password = result['password']
    command = result['command']
    data = database.cursor()
    insert = (time, service, datatype, ip, username, password, command)
    data.execute(sql, insert)
    database.commit()


def ssh_start(config, host, log_filepath, logs):
    ssh_states = config['status']
    if ssh_states == "1":
        print("service ssh start")
        ssh_port = config['port']
        host_key = config['key']
        # SSH(host, ssh_port, log_filepath, "ssh")
        ssh_process = Process(target=SSH, args=(host, ssh_port, log_filepath, host_key, "ssh", logs))
        ssh_process.start()
        return ssh_process
    return None


def smtp_start(config, host, log_filepath, logs):
    smtp_states = config['status']
    if smtp_states == "1":
        print("service redis start")
        smtp_port = config['port']
        # SMTP(host, smtp_port, log_filepath, "smtp")
        smtp_process = Process(target=SMTP, args=(host, smtp_port, log_filepath, "smtp", logs))
        smtp_process.start()
        return smtp_process
    return None


def ftp_start(config, host, log_filepath, logs):
    ftp_states = config['status']
    if ftp_states == "1":
        print("service ftp start")
        ftp_port = config['port']
        ftp_process = Process(target=FTP, args=(host, ftp_port, log_filepath, "ftp", logs))
        ftp_process.start()
        return ftp_process
    return None


def telnet_start(config, host, log_filepath, logs):
    telnet_states = config['status']
    if telnet_states == "1":
        print("service telnet start")
        telnet_port = config['port']
        telnet_process = Process(target=Telnet, args=(host, telnet_port, log_filepath, "telnet", logs))
        telnet_process.start()
        return telnet_process
    return None


def rdp_start(config, host, log_filepath, logs):
    rdp_states = config['status']
    if rdp_states == "1":
        print("service rdp start")
        rdp_port = config['port']
        # RDP(host, rdp_port, log_filepath, "rdp")
        rdp_process = Process(target=RDP, args=(host, rdp_port, log_filepath, "rdp", logs))
        rdp_process.start()
        return rdp_process
    return None


def redis_start(config, host, log_filepath, logs):
    redis_states = config['status']
    if redis_states == "1":
        print("service redis start")
        redis_port = config['port']
        # Redis(host, redis_port, log_filepath, "redis")
        redis_process = Process(target=Redis, args=(host, redis_port, log_filepath, "redis", logs))
        redis_process.start()
        return redis_process
    return None


def pop3_start(config, host, log_filepath, logs):
    pop3_states = config['status']
    if pop3_states == "1":
        print("service pop3 start")
        pop3_port = config['port']
        # POP3(host, redis_port, log_filepath, "redis")
        pop3_process = Process(target=POP3, args=(host, pop3_port, log_filepath, "pop3", logs))
        pop3_process.start()
        return pop3_process
    return None


def tftp_start(config, host, log_filepath, logs):
    tftp_states = config['status']
    if tftp_states == "1":
        print("service tftp start")
        tftp_port = config['port']
        # tftp(host, redis_port, log_filepath, "tftp")
        tftp_process = Process(target=TFTP, args=(host, tftp_port, log_filepath, "tftp", logs))
        tftp_process.start()
        return tftp_process
    return None


class Check:
    def __init__(self, main_config, service_config, config_filepath, sign):
        self.signal = 1
        self.check(main_config, service_config, config_filepath, sign)

    def check(self, main_config, service_config, config_filepath, sign):
        try:
            host = main_config['ip']
            log_filepath = main_config['path']
            logs = multiprocessing.Queue()
            database = create_db()
            print("service started, check which service is started:")

            ssh_process = ssh_start(service_config['ssh'], host, log_filepath, logs)
            smtp_process = smtp_start(service_config['smtp'], host, log_filepath, logs)
            ftp_process = ftp_start(service_config['ftp'], host, log_filepath, logs)
            telnet_process = telnet_start(service_config['telnet'], host, log_filepath, logs)
            rdp_process = rdp_start(service_config['rdp'], host, log_filepath, logs)
            redis_process = redis_start(service_config['redis'], host, log_filepath, logs)
            pop3_process = pop3_start(service_config['pop3'], host, log_filepath, logs)
            # tftp_process = tftp_start(service_config['tftp'], host, log_filepath, logs)

            print("other")
            while self.signal:
                for i in range(5):
                    try:
                        result = logs.get(timeout=0.2)
                        send_to_sql(database, result)
                        print('Result:', result)
                    except queue.Empty:
                        pass
                try:
                    message = sign.get(timeout=0.2)
                    service_config = get_config(config_filepath)
                    if message == "ssh":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        ssh_process = ssh_start(service_config['ssh'], host, log_filepath, logs)
                    if message == "smtp":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        smtp_process = smtp_start(service_config['smtp'], host, log_filepath, logs)
                    if message == "ftp":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        ftp_process = ftp_start(service_config['ftp'], host, log_filepath, logs)
                    if message == "telnet":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        telnet_process = telnet_start(service_config['telnet'], host, log_filepath, logs)
                    if message == "rdp":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        rdp_process = rdp_start(service_config['rdp'], host, log_filepath, logs)
                    if message == "redis":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        redis_process = redis_start(service_config['redis'], host, log_filepath, logs)
                    if message == "pop3":
                        if ssh_process is not None:
                            ssh_process.terminate()
                        pop3_process = pop3_start(service_config['pop3'], host, log_filepath, logs)
                    if message == 0:
                        raise NormalException
                    else:
                        print("unknown")
                except queue.Empty:
                    pass
        except NormalException:
            pass
        except KeyboardInterrupt:
            print("keyboard")
        finally:
            if ssh_process is not None:
                ssh_process.terminate()
            if smtp_process is not None:
                smtp_process.terminate()
            if ftp_process is not None:
                ftp_process.terminate()
            if telnet_process is not None:
                telnet_process.terminate()
            if rdp_process is not None:
                rdp_process.terminate()
            if redis_process is not None:
                redis_process.terminate()
            if pop3_process is not None:
                pop3_process.terminate()
            print("process closed")
