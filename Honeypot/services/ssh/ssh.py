import sys
import logging
import threading
from socket import socket, timeout
from Honeypot.services import origin_service
from datetime import datetime
import paramiko

# generate keys with 'ssh-keygen -t rsa -f server.key'
HOST_KEY = paramiko.RSAKey(filename='../server.key')


class Transport(paramiko.Transport):
    _CLIENT_ID = "OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"


class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self, logger, logs, ip):
        self.event = threading.Event()
        self.logger = logger
        self.logs = logs
        self.ip = ip

    def check_auth_password(self, username, password):
        now = datetime.now()
        info = {"time": now, "service": "ssh", "type": "login", "ip": self.ip, "username": username,
                "password": password, "command": ""}
        self.logs.put(info)
        self.logger.info("New login: username:" + username + " -- " + "password:" + password)
        return paramiko.AUTH_FAILED


def handle_connection(client, logger, host_key, logs, ip):
    transport = Transport(client)
    transport.add_server_key(host_key)
    server_handler = SSHServerHandler(logger, logs, ip)
    transport.start_server(server=server_handler)
    channel = transport.accept(20)
    if channel is not None:
        channel.close()


class SSH(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, host_key, name, logs):
        super().__init__(bind_ip, ports, log_filepath, name, logs)
        self.host_key = paramiko.RSAKey(filename=host_key)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        try:
            listener = socket()
            listener.bind((self.bind_ip, int(self.ports)))
            listener.listen(5)
            while True:
                client, addr = listener.accept()
                # self.connection_response(client, self.ports, addr[0], addr[1])
                client_handler = threading.Thread(target=self.connection_response,
                                                  args=(client, self.ports, addr[0], addr[1]))
                client_handler.start()
        except OSError:
            print("service", self.name, "find ports", self.ports, "already in used, please check again")
            print("close service", self.name)
            exit()

    def connection_response(self, client_socket, port, ip, remote_port):
        try:
            now = datetime.now()
            info = {"time": now, "service": self.name, "type": "connection", "ip": ip, "username": "", "password": "",
                    "command": ""}
            self.logs.put(info)
            self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
            client_socket.settimeout(30)
            handle_connection(client_socket, self.logger, self.host_key, self.logs, ip)
        except timeout:
            pass
        except KeyboardInterrupt:
            print('Detected interruption, terminating...')
            exit()
        except Exception as e:
            print(e)
            pass
        client_socket.close()
