import logging
import threading
from socket import socket, timeout
from services.origin_service import Service
import paramiko

# generate keys with 'ssh-keygen -t rsa -f server.key'
HOST_KEY = paramiko.RSAKey(filename='../server.key')


class Transport(paramiko.Transport):
    _CLIENT_ID = "OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"


class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self, logger):
        self.event = threading.Event()
        self.logger = logger

    def check_auth_password(self, username, password):
        logging.basicConfig(level=logging.DEBUG)
        self.logger.info("New login -  - username:" + username + " - - " + "password:" + password)
        return paramiko.AUTH_FAILED


def handle_connection(client, logger, host_key):
    transport = Transport(client)
    transport.add_server_key(host_key)
    server_handler = SSHServerHandler(logger)
    transport.start_server(server=server_handler)
    channel = transport.accept(20)
    if channel is not None:
        channel.close()


class SSH(Service):
    def __init__(self, bind_ip, ports, log_filepath, host_key, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.host_key = paramiko.RSAKey(filename=host_key)
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
            # self.connection_response(client, self.ports, addr[0], addr[1])
            client_handler = threading.Thread(target=self.connection_response,
                                              args=(client, self.ports, addr[0], addr[1]))
            client_handler.start()

    def connection_response(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        client_socket.settimeout(30)
        try:
            handle_connection(client_socket, self.logger, self.host_key)
        except timeout:
            pass
        except Exception as e:
            pass
        client_socket.close()
