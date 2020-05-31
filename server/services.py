import configparser
from multiprocessing import Process, Queue
from ..Honeypot.modify_config import reset, get_default, get_config
from ..Honeypot.checkService import Check

print("hello")

# Load config
config_filepath = "../config.ini"
configs = configparser.ConfigParser()
configs.read(config_filepath)
main_process = None
states = None

def start_services():
    states = Queue()
    main_config = get_default(config_filepath)
    service_config = get_config(config_filepath)
    main_process = Process(target=Check, args=(main_config, service_config, config_filepath, states))
    main_process.start()

    # config.set_config(states, configs, config_filepath, "ssh", "port", "2222")
    # main_process = reset(main_process, Check, states, configs, config_filepath)

def reset_config():
  main_process = reset(main_process, Check, states, configs, config_filepath)