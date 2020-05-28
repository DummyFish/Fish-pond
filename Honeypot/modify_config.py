from multiprocessing import Process
from time import sleep


def set_config(states, config, config_path, service, option, value):
    print("set")
    states.put(service)
    config.set(service, option, value)
    config.write(open(config_path, "w"))


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
    process = Process(target=check, args=(config_path, states))
    process.start()
    return process
