import fakeredis
import logging
from twisted.python import failure
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor, error
from services.origin_service import Service


class RedisServer(Protocol):
    connectionNb = 0

    def __init__(self, logger, name, port):
        self.logger = logger
        self.command = ['get', 'set', 'config', 'quit', 'ping', 'del', 'keys', "save", "flushall", "flushdb"]
        self.name = name
        self.port = port
        self.r = fakeredis.FakeStrictRedis()

    def connectionMade(self):
        self.connectionNb += 1
        self.logger.info("Connection received to service %s:%d  %s:%d" % (
            self.name, self.port, self.transport.getPeer().host, self.transport.getPeer().port))

    def dataReceived(self, rcvdata):
        cmd_count = 0
        cmd_count += 1
        command = rcvdata.decode("utf-8")
        if command is '\n' or '\r\n':
            pass
        else:
            data = command.split()
            msg = None
            self.logger.info("received command: %s" % str(command))
            if data[0] in self.command:
                if data[0].lower() == "quit":
                    self.transport.loseConnection()
                elif data[0].lower() == "ping":
                    msg = b"+PONG"
                    self.logger.info("send message: %s" % msg)
                    self.transport.write(msg)
                elif data[0].lower() == "save" or data[0].lower() == "flushall" or data[0].lower() == "flushdb":
                    self.logger.info("send message: %s" % msg)
                    self.transport.write(msg)
                    msg = b"+OK"
                    self.logger.info("send message: %s" % msg)
                    self.transport.write(msg)
                else:
                    if command.lower().startswith('config get') and len(data) == 3:
                        msg = "-(error) ERR Unsupported CONFIG parameter: {0}".format(data[2]).encode('utf-8')
                        self.logger.info("send message: %s" % msg)
                        self.transport.write(msg)
                    elif command.lower().startswith('config set') and len(data) == 4:
                        msg = "-(error) ERR Unsupported CONFIG parameter: {0}".format(data[2]).encode('utf-8')
                        self.logger.info("send message: %s" % msg)
                        self.transport.write(msg)
                    elif data[0].lower() == "set" and len(data) == 3:
                        if self.r.set(data[1], data[2]):
                            msg = b"+OK"
                            self.logger.info("send message: %s" % msg)
                            self.transport.write(msg)
                    elif data[0].lower().startswith('del') and len(data) == 2:
                        if self.r.delete(data[1]):
                            msg = b"+(integer) 1"
                            self.logger.info("send message: %s" % msg)
                            self.transport.write(msg)
                        else:
                            msg = b"+(integer) 0"
                            self.logger.info("send message: %s" % msg)
                            self.transport.write(msg)
                    elif data[0].lower() == 'get' and len(data) == 2:
                        if self.r.get(data[1]):
                            s = self.r.get(data[1])
                            msg = "+{0}".format(s).encode('utf-8')
                            self.logger.info("send message: %s" % msg)
                            self.transport.write(msg)
                        else:
                            msg = b"+(nil)"
                            self.logger.info("send message: %s" % msg)
                            self.transport.write(msg)
                    else:
                        msg = "-ERR wrong number of arguments for '{0}' command".format(data[0]).encode('utf-8')
                        self.logger.info("send message: %s" % msg)
                        self.transport.write(msg)
            else:
                msg = "-ERR unknown command '{0}'".format(data[0]).encode('utf-8')
                self.logger.info("send message: %s" % msg)
                self.transport.write(msg)

    def connectionLost(self, reason):
        self.connectionNb -= 1
        self.logger.info("End connection: ", reason.getErrorMessage())


class RedisServerFactory(ServerFactory):
    protocol = RedisServer

    def __init__(self, logger, name, port):
        self.logger = logger
        self.name = name
        self.port = port

    def buildProtocol(self, addr):
        p = self.protocol(self.logger, self.name, self.port)
        p.factory = self
        return p


class Redis(Service):
    def __init__(self, bind_ip, ports, log_filepath, name):
        super().__init__(bind_ip, ports, log_filepath, name)
        self.service_start()

    def service_start(self):
        print(self.name, "started on port", self.ports)
        self.start_listen()

    def start_listen(self):
        reactor.listenTCP(self.ports, RedisServerFactory(self.logger, self.name, self.ports))
        try:
            reactor.run()
        except KeyboardInterrupt:
            print('Detected interruption, terminating...')
        except Exception as e:
            pass
