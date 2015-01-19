from tank.motors import Motors
from tank.application import Application


def main():
    motors = Motors('10.10.1.1')
    app = Application(motors)
    app.main()

if __name__ == '__main__':
    main()
