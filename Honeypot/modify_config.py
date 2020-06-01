from multiprocessing import Process
from time import sleep
import configparser


def get_default(config_path):
    configs = configparser.ConfigParser()
    configs.read(config_path)
    host = configs.get('default', 'host', raw=True, fallback="0.0.0.0")
    log_filepath = configs.get('default', 'logfile', raw=True, fallback="./logfile.log")
    default = {
        'id': 'honeypot',
        'path': log_filepath,
        'ip': '0.0.0.0'
    }
    return default


def get_config(config_path):
    configs = configparser.ConfigParser()
    configs.read(config_path)
    ssh_states = configs.get('ssh', 'status', raw=True, fallback="0")
    ssh_port = configs.get('ssh', 'port', raw=True, fallback="22")
    host_key = configs.get('ssh', 'service_key', raw=True, fallback="../server.key")
    smtp_states = configs.get('smtp', 'status', raw=True, fallback="0")
    smtp_port = configs.get('smtp', 'port', raw=True, fallback="2525")
    ftp_states = configs.get('ftp', 'status', raw=True, fallback="0")
    ftp_port = configs.get('ftp', 'port', raw=True, fallback="21")
    telnet_states = configs.get('telnet', 'status', raw=True, fallback="0")
    telnet_port = configs.get('telnet', 'port', raw=True, fallback="23")
    rdp_states = configs.get('rdp', 'status', raw=True, fallback="0")
    rdp_port = configs.get('rdp', 'port', raw=True, fallback="3389")
    redis_states = configs.get('redis', 'status', raw=True, fallback="0")
    redis_port = configs.get('redis', 'port', raw=True, fallback="6379")
    pop3_states = configs.get('pop3', 'status', raw=True, fallback="0")
    pop3_port = configs.get('pop3', 'port', raw=True, fallback="995")
    tftp_states = configs.get('tftp', 'status', raw=True, fallback="0")
    tftp_port = configs.get('tftp', 'port', raw=True, fallback="69")
    honeypot_config = {
        'ssh': {'id': 'ssh', 'status': ssh_states, 'port': ssh_port, 'key': host_key},
        'smtp': {'id': 'smtp', 'status': smtp_states, 'port': smtp_port},
        'ftp': {'id': 'ftp', 'status': ftp_states, 'port': ftp_port},
        'telnet': {'id': 'telnet', 'status': telnet_states, 'port': telnet_port},
        'rdp': {'id': 'rdp', 'status': rdp_states, 'port': rdp_port},
        'redis': {'id': 'redis', 'status': redis_states, 'port': redis_port},
        'pop3': {'id': 'pop3', 'status': pop3_states, 'port': pop3_port},
        'tftp': {'id': 'tftp', 'status': tftp_states, 'port': tftp_port},
    }
    return honeypot_config


def set_config(states, config, config_path, service, option, value):
    states.put(service)
    config.set(service, option, value)
    config.write(open(config_path, "w"))
    return get_config(config_path)


def reset(process, check, states, config, config_path):
    states.put(0)
    sleep(2)
    config.set("default", "logfile", "../logfile.log")
    config.set("default", "host", "0.0.0.0")
    config.set("ssh", "status", "1")
    config.set("ssh", "port", "22")
    config.set("smtp", "status", "1")
    config.set("smtp", "port", "25")
    config.set("ftp", "status", "1")
    config.set("ftp", "port", "21")
    config.set("telnet", "status", "1")
    config.set("telnet", "port", "23")
    config.set("rdp", "status", "1")
    config.set("rdp", "port", "3390")
    config.set("redis", "status", "1")
    config.set("redis", "port", "6379")
    config.set("pop3", "status", "1")
    config.set("pop3", "port", "995")
    config.set("tftp", "status", "1")
    config.set("tftp", "port", "69")
    config.write(open(config_path, "w"))
    process.close()
    main_config = get_default(config_path)
    service_config = get_config(config_path)
    process = Process(target=check, args=(main_config, service_config, config_path, states))
    process.start()
    return process
