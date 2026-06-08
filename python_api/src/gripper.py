# robot_api/gripper.py
from std_msgs.msg import Bool

class Gripper:
    def __init__(self, node):
        self.node = node
        self.pub = node.create_publisher(Bool, '/hal_io/dout01', 10)

    def open(self):
        msg = Bool()
        msg.data = False
        self.pub.publish(msg)

    def close(self):
        msg = Bool()
        msg.data = True
        self.pub.publish(msg)