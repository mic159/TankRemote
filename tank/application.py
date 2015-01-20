import pygtk
pygtk.require('2.0')
import gtk
from tank.motors import Motors, DEFAULT_IP


class Application(object):
    def __init__(self, motors, video):
        self.motors = motors
        self.video = video
        self.ip_box = None

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('WiFi Tank Remote')
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        layout = gtk.VBox(False, 5)

        self.connect_box = self.setup_connection_box()
        layout.add(self.connect_box)

        self.direction_pad = self.setup_direction_pad()
        layout.add(self.direction_pad)

        self.vid_img = self.setup_video_image()
        layout.add(self.vid_img)

        layout.show()
        self.window.add(layout)

        self.motors.connect('connected', self.on_connection_state_change)

        self.window.show()

    def setup_direction_pad(self):
        box = gtk.VBox(False, 0)
        button_config = [
            [
                ('Forward', ((Motors.LEFT, Motors.FORWARD),
                             (Motors.RIGHT, Motors.FORWARD)))
            ],
            [
                ('Left',    ((Motors.LEFT, Motors.BACK),
                             (Motors.RIGHT, Motors.FORWARD))),
                ('Stop',   ((Motors.LEFT, Motors.STOP),
                            (Motors.RIGHT, Motors.STOP))),
                ('Right',   ((Motors.LEFT, Motors.FORWARD),
                             (Motors.RIGHT, Motors.BACK)))
            ],
            [
                ('Back',    ((Motors.LEFT, Motors.BACK),
                             (Motors.RIGHT, Motors.BACK)))
            ],
        ]

        for buttons_set in button_config:
            hbox = gtk.HBox(False, 0)
            box.pack_start(hbox, True, True, 0)
            for title, commands in buttons_set:
                inst = gtk.Button(title)
                inst.connect('clicked', self.send_command, commands)
                inst.show()
                hbox.pack_start(inst, True, True, 0)
            hbox.show()

        box.set_sensitive(False)
        box.show()
        return box

    def setup_connection_box(self):
        box = gtk.HBox(False, 0)
        self.ip_box = gtk.Entry(16)
        self.ip_box.set_text(DEFAULT_IP)
        self.ip_box.show()
        box.pack_start(self.ip_box, True, True, 0)

        connect_btn = gtk.Button('Connect')
        connect_btn.connect('clicked', self.on_click_connect)
        connect_btn.show()
        box.pack_start(connect_btn, True, True, 0)

        box.show()
        return box

    def setup_video_image(self):
        img = gtk.Image()
        img.show()
        self.video.widget = img
        return img

    def send_command(self, _, data=None):
        for cmd in data:
            self.motors.command(cmd[0], cmd[1])

    def on_connection_state_change(self, _, connected):
        self.direction_pad.set_sensitive(connected)
        self.connect_box.set_sensitive(not connected)

    def on_click_connect(self, _, data=None):
        self.motors.init_connection(self.ip_box.get_text())
        self.video.init_connection(self.ip_box.get_text())

    def destroy(self, _, data=None):
        gtk.main_quit()
