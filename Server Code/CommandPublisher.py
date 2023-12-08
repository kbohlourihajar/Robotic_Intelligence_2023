import rclpy
from rclpy.node import Node
import json

from std_msgs.msg import String


class CommandPublisher(Node):

    def __init__(self):
        super().__init__('command_publisher')
        self.publisher_ = self.create_publisher(String, '/command', 10)
        timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = self.command
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

    def publish_command(self, command):
        msg = String()
        msg.data = json.dumps(command)
        self.publisher_.publish(msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = CommandPublisher()

    try:
        while True:
            command = input("give a command: ")
            minimal_publisher.publish_command(command)
    except KeyboardInterrupt:
        pass

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
