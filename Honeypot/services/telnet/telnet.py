import sys
import logging
import threading
from datetime import datetime
from socket import socket, timeout, SHUT_RDWR
from services import origin_service
import telnetlib3


class TelneterverHandler(telnetlib3.TelnetServer):
    def __init__(self, logger, logs, ip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = threading.Event()
        self.logger = logger
        self.logs = logs
        self.ip = ip

    def check_auth_password(self, username, password):
        now = datetime.now()
        info = {"time": now, "service": "ssh", "type": "login", "ip": self.ip, "username": username,
                "password": password}
        self.logs.put(info)
        self.logger.info("New login -  - username:" + username + " - - " + "password:" + password)
        return False


def handle_connection(client, logger, logs, ip):
    # unusable temperally change to no interaction log
    while True:
        try:
            rcvdata = client.recv(1024).decode("utf-8").replace("\n", "")
            now = datetime.now()
            info = {"time": now, "service": "telnet", "type": "command", "ip": ip, "username": "",
                    "password": "", "command": rcvdata}
            logs.put(info)
            logger.info("received command: %s" % rcvdata)
        except KeyboardInterrupt:
            client.shutdown(SHUT_RDWR)
            client.close()
    # transport = telnetlib3.TelnetServer.connection_made(client)
    # server_handler = TelnetServerHandler(logger)
    # transport.start_server(server=server_handler)
    # channel = transport.accept(20)
    # if channel is not None:
    #     channel.close()


class Telnet(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, name, logs):
        super().__init__(bind_ip, ports, log_filepath, name, logs)
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
        now = datetime.now()
        info = {"time": now, "service": self.name, "type": "connection", "ip": ip, "username": "",
                "password": "", "command": ""}
        self.logs.put(info)
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        client_socket.settimeout(30)
        try:
            handle_connection(client_socket, self.logger, self.logs, ip)
        except timeout:
            pass
        except KeyboardInterrupt:
            print('Detected interruption, terminating...')
            client_socket.close()
        except Exception as e:
            pass
        client_socket.close()
