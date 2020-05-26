import logging
import threading
from socket import socket, timeout


class Service(object):
    def __init__(self, bind_ip, ports, log_filepath, name, logs):
        if len(ports) < 1:
            raise Exception("No ports provided.")
        self.name = name
        self.bind_ip = bind_ip
        self.ports = int(ports)
        self.log_filepath = log_filepath
        self.logs = logs
        self.logger = self.prepare_logger()

    def prepare_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
                            datefmt="%d-%m-%Y %H:%M:%S",
                            filename=self.log_filepath)
        logger = logging.getLogger(self.name)

        # Adding console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        logger.info("service %s initializing...", self.name)
        logger.info("Ports: %d" % self.ports)
        logger.info("Log filepath: %s" % self.log_filepath)
        return logger
