import socket

CONTROL_PORT = 8150


class Motors(object):
    LEFT = 1
    RIGHT = 2

    FORWARD = 1
    BACK = 2
    STOP = 0

    def __init__(self, ip, port=CONTROL_PORT):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.connect()

    def connect(self):
        print 'Connecting to', self.ip
        self.connection.connect((self.ip, self.port))
        self.connection.sendall('t1')
        print 'Connected'

    def command(self, motor, direction):
        self.connection.sendall('%i%i' % (motor, direction))
