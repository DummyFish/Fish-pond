import configparser
from multiprocessing import Process, Queue
from Honeypot.modify_config import reset, get_default, get_config
from Honeypot.checkService import Check

print("hello")


def reset_config(main_process, states, configs, config_filepath):
  main_process = reset(main_process, Check, states, configs, config_filepath)