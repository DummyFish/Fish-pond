import sys
import logging
import threading
from socket import socket, timeout, AF_INET, SOCK_STREAM, SHUT_RDWR
from services import origin_service


class TFTPprotocal:
    def __init__(self, server_socket):
        self.login = False
        self.server_socket = server_socket


    def interact(self, incomedata):
        return 'please enter the correct commend'


def TFTPserver_thread(client_socket, logger):
    client_socket.send(bytes('* OK TFTP Service is ready\n',"utf-8"))
    try:
        # while not auth:
        client_socket.send(b'tftp server:')
        manager =TFTPprotocal(client_socket)
        logger.info("New login\n")
        while 1:
            incomingData = str(client_socket.recv(1024), "utf-8").replace("\n", "").replace("\r", "")
            logger.info("new command " + incomingData)
            outgoingData = manager.interact(incomingData)
            client_socket.send(bytes(outgoingData + "\n", "utf-8"))

    except KeyboardInterrupt:
        client_socket.shutdown(SHUT_RDWR)
        client_socket.close()


class TFTP(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind((self.bind_ip, int(self.ports)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            self.waitforconnection(client, self.ports, addr[0], addr[1])

    def waitforconnection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        TFTPserver_thread(client_socket, self.logger)