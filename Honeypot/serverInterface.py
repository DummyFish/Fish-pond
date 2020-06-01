import configparser
from multiprocessing import Process, Queue
from Honeypot.modify_config import reset, get_default, get_config, set_config
from Honeypot.checkService import Check
from Honeypot.analysis import get_latest_log, check_service_num

latest_date = ''
print("Start honeypot")
config_filepath = "../config.ini"
configs = configparser.ConfigParser()
configs.read(config_filepath)
main_process = None
states = Queue()
main_config = get_default(config_filepath)
service_config = get_config(config_filepath)
main_process = Process(target=Check, args=(main_config, service_config, config_filepath, states))
print("Start services...")
main_process.start()
print("Done initialization")

def reset_api(main_process = main_process, Check = Check, states = states, configs = configs, config_filepath = config_filepath):
    main_process = reset(main_process, Check, states, configs, config_filepath)

def set_config_api(serviceName, configType, configVal, states = states, configs = configs, config_filepath = config_filepath):
    set_config(states, configs, config_filepath, serviceName, configType, configVal)

def get_logs_api(latest_date = latest_date):
    if (latest_date == ''):
        data = get_latest_log()
    else:
        data = get_latest_log(latest_date)
    latest_date = data[0][1]
    logs = []
    index = 1
    for log in data:
        # print("LOG: ")
        # print(log)
        logs.append({'id': index, 'ip': log[4], 'service': log[2], 'time': log[1], 'meta': log[3]})
        index += 1
    return logs

def get_service_stats_api():
    return check_service_num()

def get_honeypot_config_api(config_filepath = config_filepath):
    return get_default(config_filepath)

def get_service_config_api(config_filepath = config_filepath):
    return get_config(config_filepath)