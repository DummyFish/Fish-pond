import sys
import logging
import threading
from datetime import datetime
from socket import socket, timeout, AF_INET, SOCK_STREAM, SHUT_RDWR
from Honeypot.services import origin_service


class POP3protocal:
    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.auth = False

    def autheticate(self, user, password):
        self.server_socket.send('welcome\n'.encode())
        self.auth = True

    def interact(self, incomedata):
        logger.info("received command: " + incomedata)
        return 'commend ' + incomedata + ' not found please try again '


def POP3server_thread(client_socket, logger, logs, ip):
    client_socket.send('* OK POP Service is ready\n'.encode())
    try:
        client_socket.send(b"please enter username:")
        username = str(client_socket.recv(1024), "utf-8").replace("\n", "").replace("\r", "")
        client_socket.send(b"please enter password:")
        password = str(client_socket.recv(1024), "utf-8").replace("\n", "").replace("\r", "")
        now = datetime.now()
        info = {"time": now, "service": "pop3", "type": "login", "ip": ip, "username": username,
                "password": password, "command": ""}
        logs.put(info)
        logger.info("New login - - username: " + username + " - - " + "password: " + password)
        manager = POP3protocal(client_socket)
        manager.autheticate(username, password)

        while 1:
            incomingData = str(client_socket.recv(1024), "utf-8").replace("\n", "").replace("\r", "")
            if not incomingData:
                break
            outgoingData = manager.interact(incomingData, logger)
            if not outgoingData:
                break
            client_socket.send(bytes(outgoingData + "\n", "utf-8"))
    except KeyboardInterrupt:
        client_socket.shutdown(SHUT_RDWR)
        client_socket.close()


class POP3(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, name, logs):
        super().__init__(bind_ip, ports, log_filepath, name, logs)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        try:
            listener = socket(AF_INET, SOCK_STREAM)
            listener.bind((self.bind_ip, int(self.ports)))
            listener.listen(5)
            while True:
                client, addr = listener.accept()
                self.waitforconnection(client, self.ports, addr[0], addr[1])
        except OSError:
            print("service", self.name, "find ports", self.ports, "already in used, please check again")
            print("close service", self.name)
            exit()

    def waitforconnection(self, client_socket, port, ip, remote_port):
        now = datetime.now()
        info = {"time": now, "service": self.name, "type": "connection", "ip": ip, "username": "",
                "password": "", "command": ""}
        self.logs.put(info)
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        POP3server_thread(client_socket, self.logger, self.logs, ip)
