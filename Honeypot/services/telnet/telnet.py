import sys
import logging
import threading
from socket import socket, timeout
from origin_service import Service
import telnetlib3




class TelneterverHandler(telnetlib3.TelnetServer):
    def __init__(self, logger):
        self.event = threading.Event()
        self.logger = logger

    def check_auth_password(self, username, password):
        logging.basicConfig(level=logging.DEBUG)
        self.logger.info("New login -  - username:" + username + " - - " + "password:" + password)
        return False
    


def handle_connection(client, logger):
    transport = telnetlib3.TelnetServer.connection_made(client)
    server_handler = TelnetServerHandler(logger)
    transport.start_server(server=server_handler)
    channel = transport.accept(20)
    if channel is not None:
        channel.close()


class Telnet(Service):
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
