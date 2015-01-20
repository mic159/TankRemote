import gtk
import gobject
from tank.motors import Motors
from tank.video import Video
from tank.application import Application


def main():
    gobject.threads_init()
    motors = Motors()
    video = Video()
    app = Application(motors, video)
    gtk.main()
    if video.thread:
        video.thread.quit = True

if __name__ == '__main__':
    main()
