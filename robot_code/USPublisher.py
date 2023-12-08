import rclpy
from rclpy.node import Node
import ultrasonic

from std_msgs.msg import Float64


class UltrasonicPublisher(Node):

    def __init__(self):
        super().__init__('ultrasonic_publisher')
        self.publisher_ = self.create_publisher(Float64, '/command', 1)

    def publish_ultrasonic(self):
        msg = Float64()
        msg.data = ultrasonic.distance()
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    ultrasonic_pub = UltrasonicPublisher()

    while True:
        ultrasonic_pub.publish_ultrasonic()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ultrasonic_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()