import sys, time, Leap
from cflib import crtp
from threading import Thread
from cflib.crazyflie import Crazyflie

# 65365.0
MAX_THRUST = 60000
MAX_YAW = 20.0
MAX_PITCH = 20.0
MAX_ROLL = 20.0


class CrazyFlieController:
    def __init__(self, link_uri):
        self._crazyflie = Crazyflie()

        self._crazyflie.connected.add_callback(self._connected)
        self._crazyflie.open_link(link_uri)
        self._crazyflie.commander.set_client_xmode(True)

    def listen_command(self, roll, pitch, yaw, thrust):
        print(roll, pitch, yaw, thrust * MAX_THRUST)
        self._crazyflie.commander.send_setpoint(roll * 20, pitch * 20, yaw, thrust * MAX_THRUST)
        time.sleep(0.001)

    def _connected(self, link_uri):
        thread = Thread(target=self.listen_command)
        thread.start()

    def _disconnected(self, link_uri):
        print('Disconnected from %s ' % link_uri)

    def _conntion_failed(self, link_uri, msg):
        print('Connection to %s failed: %s' % (link_uri, msg))


class LeapListener(Leap.Listener):

    def callback(self, callback):
        self._callback = callback

    def on_init(self, controller):
        print("Initialised")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, arg0):
        print("Disconnected")

    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            if hand.is_right:
                normal = hand.palm_normal
                direction = hand.direction


                '''
                roll = -direction.pitch * Leap.RAD_TO_DEG / 30.0
                pitch = -normal.roll * Leap.RAD_TO_DEG / 30.0

                '''
                pitch = -direction.pitch * Leap.RAD_TO_DEG / 30.0
                roll = -normal.roll * Leap.RAD_TO_DEG / 30.0

                yaw = direction.yaw * Leap.RAD_TO_DEG / 70.0
                thrust = (hand.palm_position[1] - 80) / 150.0

                if thrust < 0.0:
                    thrust = 0.0
                if thrust > 1.0:
                    thrust = 1.0

                if len(hand.fingers) < 4:
                    self._callback(0, 0, 0, 0)
                else:
                    self._callback(roll, pitch, yaw, thrust)
            else:
                self._callback(0, 0, 0, 0)

        if len(frame.hands) == 0:
            self._callback(0, 0, 0, 0)


class LeapController:

    def __init__(self, link_uri):

        self.data = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0, 'thrust': 0.0, 'pitchcal': 0.0, 'rollcal': 0.0, 'estop': False, 'exit': False}

        self._listener = LeapListener()
        self._listener.callback(self.leap_callback)
        self._controller = Leap.Controller()
        self._controller.add_listener(self._listener)

        self._crazyflie_controller = CrazyFlieController(link_uri)

    def leap_callback(self, roll, pitch, yaw, thrust):

        self._crazyflie_controller.listen_command(roll, pitch, yaw, thrust)

    def read_input(self):
        self.data['pitchcal'] = 0.0
        self.data['rollcal'] = 0.0

        return self.data


def main():

    while True:

        sys.stdout.write("\r" + str(leap_controller.read_input()))
        sys.stdout.flush()

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        pass
        # controller.remove_listener(listener)

if __name__ == '__main__':

    crtp.init_drivers(enable_debug_driver=False)
    available = crtp.scan_interfaces()

    for i in available:
        print(i[0])

    if len(available) > 0:
        print("available", available[0][0])
        leap_controller = LeapController(available[0][0])
    else:
        print('No Crazyflies found, cannot run example')



