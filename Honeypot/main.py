from checkService import check
import configparser
from multiprocessing import Process, Queue
from modify_config import reset

print("hello")

# Load config
config_filepath = "../config.ini"
configs = configparser.ConfigParser()
configs.read(config_filepath)

if __name__ == '__main__':
    states = Queue()
    main_process = Process(target=Check, args=(config_filepath, states))
    main_process.start()

    # config.set_config(states, configs, config_filepath, "ssh", "port", "2222")
    main_process = reset(main_process, Check, states, configs, config_filepath)
