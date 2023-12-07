import rclpy
from rclpy.node import Node
import json

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class SimplePub(Node):

    def __init__(self, command):
        super().__init__('command_publisher')
        self.command = json.dumps(command)
        self.publisher_ = self.create_publisher(Image, '/random', 1)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.bridge = CvBridge()
        self.camera = cv2.VideoCapture(0)


    def timer_callback(self):
        try:
            # Convert your ROS Image message to OpenCV2
            ret, image = self.camera.read()
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(image, "bgr8"))
            print(f"published {self.i}")
            self.get_logger().info(f"publishing: {self.i}")
        except CvBridgeError as e:
            print(e)
        self.i += 1

    def publish_command(self, command):
        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = SimplePub("lorem ipsum")

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()