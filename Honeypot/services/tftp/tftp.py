import sys
import os
import logging
import threading
from pathlib import Path
from socket import socket, timeout
from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer
from services import origin_service

sys.path.append('..')

 
class TFTP(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):

        handler = BaseHandler
        address = (self.bind_ip,self.ports)
        server = BaseServer(address,handler)
        handler.timeout = 600
        server.max_cons = 256
        server.max_cons_per_ip = 5
        self.logger.info("Connection received to service %s:%d  %s" % (self.name, self.ports, self.bind_ip))
        try:
            server.serve_forever()
        except timeout:
            pass
        except Exception as e:
            pass
        except KeyboardInterrupt:
            print('Detected interruption, terminating...')


