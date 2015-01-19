import pygtk
pygtk.require('2.0')
import gtk
from tank.motors import Motors


class Application(object):
    def __init__(self, motors):
        self.motors = motors
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('WiFi Tank Remote')
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.box = gtk.VBox(False, 0)
        self.window.add(self.box)

        buttons = [
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

        for buttons_set in buttons:
            hbox = gtk.HBox(False, 0)
            self.box.pack_start(hbox, True, True, 0)
            for title, commands in buttons_set:
                inst = gtk.Button(title)
                inst.connect('clicked', self.send_command, commands)
                hbox.pack_start(inst, True, True, 0)
                inst.show()

            hbox.show()

        self.box.show()
        self.window.show()

    def send_command(self, widget, data=None):
        for cmd in data:
            self.motors.command(cmd[0], cmd[1])

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()