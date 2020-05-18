import socket
import threading
from socket import timeout
from services.origin_service import Service
from base64 import b64encode
import re


def extract_username(data):
    match = re.search(rb'mstshash=(?P<username>[a-zA-Z0-9-_@]+)', data)
    if match:
        username = match.group('username').decode("utf-8")
        return username
    return None


def handle_connection(client_socket, logger):
    data = client_socket.recv(4096)
    length = str(len(data))
    encode_data = b64encode(data).decode("utf-8")

    username = extract_username(data)
    if username:
        logger.info("username: " + username)
    logger.info("receive data: " + encode_data)
    client_socket.send(b"0x00000004 RDP_NEG_FAILURE")
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    logger.info("Close connection and restart...")


class RDP(Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        listener = socket.socket()
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
            handle_connection(client_socket, self.logger)
        except timeout:
            print('timeout, terminating...')
            pass
        except KeyboardInterrupt:
            print('Detected interruption, terminating...')
            client_socket.close()

        client_socket.close()
