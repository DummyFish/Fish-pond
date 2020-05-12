import sys
import logging
import threading
from socket import socket, timeout
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from services.origin_service import Service

sys.path.append('..')


class FakeAuthorizer(DummyAuthorizer):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def validate_authentication(self, username, password, handler):
        self.logger.info("New login -  - username:" + username + " - - " + "password:" + password)
        raise AuthenticationFailed


def handle_connection(client, logger):
    authorizer = FakeAuthorizer(logger)
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(client, handler)
    server.serve_forever()


class FTP(Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        listener = socket()
        listener.bind((self.bind_ip, int(self.ports)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            client_handler = threading.Thread(target=self.connection_response,
                                              args=(client, self.ports, addr[0], addr[1]))
            client_handler.start()

    def connection_response(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        client_socket.settimeout(30)
        try:
            handle_connection(client_socket, self.logger)
        except timeout:
            pass
        except Exception as e:
            pass
        client_socket.close()
