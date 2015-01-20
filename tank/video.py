import threading
import gobject
import urllib
import gtk

VIDEO_PORT = 8196


class Video(gobject.GObject):
    '''
    Connect to the MJPEG stream of the tank!
    '''
    def __init__(self, port=VIDEO_PORT):
        self.__gobject_init__()
        self.port = port
        self.stream = None
        self.thread = None
        self.widget = None
        self.buffer = ''

    def init_connection(self, ip):
        print 'Connecting to video on', ip
        self.stream = urllib.urlopen('http://%s:%d/' % (ip, self.port))
        print 'Starting video thread'
        self.thread = VideoThread(self, self.widget)
        self.thread.start()
        print 'connected'

    def get_raw_frame(self):
        '''
        Parse an MJPEG http stream and yield each frame.

        :return: generator of JPEG images
        '''
        while True:
            self.buffer += self.stream.read(1034)
            a = self.buffer.find('\xff\xd8')
            b = self.buffer.find('\xff\xd9')
            if a != -1 and b != -1:
                frame = self.buffer[a:b+2]
                self.buffer = self.buffer[b+2:]
                yield frame


class VideoThread(threading.Thread):
    '''
    A background thread that takes the MJPEG stream and
    updates the GTK image.
    '''
    def __init__(self, video, widget):
        super(VideoThread, self).__init__()
        self.video = video
        self.widget = widget
        self.quit = False

    def run(self):
        for frame in self.video.get_raw_frame():
            if self.quit:
                return
            loader = gtk.gdk.PixbufLoader('jpeg')
            loader.write(frame)
            loader.close()
            pixbuf = loader.get_pixbuf()
            gobject.idle_add(self.widget.set_from_pixbuf, pixbuf)
