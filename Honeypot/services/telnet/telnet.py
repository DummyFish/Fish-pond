import sys
import logging
import threading
import signal
from services.origin_service import Service
import os
import configparser

sys.path.append('..')

def signal_handler(signal, frame):
    print("\nClosing out cleanly...")
    telnet_server.SERVER_RUN = False

def define_logger(settings):
    FORMAT = '%(asctime)s - %(name)s - %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format=FORMAT)

    try:
        infohandler = logging.FileHandler(settings['log_location'])
    except:
        infohandler = logging.FileHandler("telnet-log.txt")
    infohandler.setLevel(logging.INFO)
    infohandler.setFormatter(logging.Formatter(FORMAT))

    debughandler = logging.StreamHandler()
    debughandler.setLevel(logging.DEBUG)

    logger = logging.getLogger(settings['hostname'])
    logger.addHandler(infohandler)

    logging.getLogger("requests").setLevel(logging.WARNING)


def parse_config():

    settings = {}
    config = configparser.ConfigParser()
    config.read('telnet.cfg')
    settings['port'] = config.getint('Telnet', 'port')
    settings['image'] = config.get('Telnet', 'image')
    settings['passwordmode'] = config.getboolean('Telnet', 'password-mode')
    settings['hostname'] = config.get('Telnet', 'hostname')
    settings['log_location'] = config.get('Telnet', 'log')
    settings['address'] = config.get('Telnet', 'address')

    return settings

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)

    settings = parse_config()

    define_logger(settings)

    telnet_server = Service(
        hostname = settings['hostname'],
        port = settings['port'],
        address = settings['address'],
        image = settings['image'],
        passwordmode = settings['passwordmode'],
    )

    logger = logging.getLogger(settings['hostname'])
    logger.info("[SERVER] Listening for connections on port {}. CTRL-C to break.".
                format(telnet_server.port))
    while telnet_server.SERVER_RUN is True:
        telnet_server.poll()
        telnet_server.kick_idle()
        telnet_server.process_clients()

    telnet_server.clean_exit()
