import sys
import logging
import threading
from socket import socket, timeout, AF_INET, SOCK_STREAM, SHUT_RDWR
from services import origin_service


class POP3protocal:
    def  __init__(self,server_socket):
        self.login = False
        self.server_socket = server_socket
    def autheticate(self,user,password):
        self.server_socket.send('invalid credential, please try again\n'.encode())
        self.server_socket.shutdown(SHUT_RDWR)
        self.server_socket.close()
    def interact(self,incomedata):
        return 'Fail'

def POP3server_thread(client_socket, logger):
    print("Allocating a new thread for the connection that was just recieved")
    print('-------------------------------------------------------')
    client_socket.send('* OK POP Service is ready\n'.encode())
    auth = False
    while auth != True:
        client_socket.send('please enter username:\n'.encode())
        username = str(client_socket.recv(1024), "utf-8")
        client_socket.send('please enter password:\n'.encode())
        password = str(client_socket.recv(1024),"utf-8")
        logger.info("New login -  - username:" + username + " - - " + "password:" + password)
        manager = POP3protocal(client_socket)
        auth = manager.autheticate(username,password)

    try:
        while 1:
            incomingData = str(client_socket.recv(1024), "utf-8")
            if not incomingData:
                break
            outgoingData = manager.interact(incomingData)
            if not outgoingData:
                break
            client_socket.send(bytes(outgoingData + "\n", "utf-8")) 
    except KeyboardInterrupt:
        client_socket.shutdown(SHUT_RDWR)
        client_socket.close()





class POP3(origin_service.Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        listener = socket(AF_INET,SOCK_STREAM)
        listener.bind((self.bind_ip, int(self.ports)))
        listener.listen(5)
        print('POP3 Server is now taking requests')
        print("==============================================")
        while True:
            client, addr = listener.accept()
            # self.connection_response(client, self.ports, addr[0], addr[1])
            client_handler = threading.Thread(target=self.waitforconnection,
                                              args=(client, self.ports, addr[0], addr[1]))
            client_handler.start()

    def waitforconnection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received to service %s:%d  %s:%d" % (self.name, port, ip, remote_port))
        client_socket.settimeout(30)

        POP3server_thread(client_socket,self.logger)
