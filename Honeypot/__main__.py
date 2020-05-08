import configparser
import sys
from Honeypot import checkService

print("hello")

# Load config
config_filepath = "../config.ini"
config = configparser.ConfigParser()
config.read(config_filepath)

if __name__ == '__main__':
    checkService.check(config)
