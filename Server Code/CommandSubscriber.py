import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import time

class CommandSubscriber(Node):
    def __init__(self):
        super().__init__('command_listener')
        self.subscription = self.create_subscription(
            String,
            '/command',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f"received command: {msg.data}")
        print(f"received command: {msg.data}")

def main(args=None):
    rclpy.init(args=args)

    image_saver = CommandSubscriber()

    rclpy.spin(image_saver)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()