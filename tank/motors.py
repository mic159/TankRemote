import socket
import gobject

CONTROL_PORT = 8150
DEFAULT_IP = '10.10.1.1'


class Motors(gobject.GObject):
    LEFT = 1
    RIGHT = 2
    CAMERA = 3

    FORWARD = 1
    BACK = 2
    STOP = 0

    def __init__(self, port=CONTROL_PORT):
        self.__gobject_init__()
        self.is_connected = False
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def init_connection(self, ip):
        print 'Connecting to', ip
        self.connection.connect((ip, self.port))
        self.connection.sendall('t1')
        self.is_connected = True
        self.emit('connected', True)
        print 'Connected'

    def command(self, motor, direction):
        try:
            self.connection.sendall('%i%i' % (motor, direction))
        except IOError:
            self.emit('connected', False)
            self.is_connected = False

gobject.type_register(Motors)
gobject.signal_new("connected", Motors, gobject.SIGNAL_RUN_FIRST,
                   gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN, ))
