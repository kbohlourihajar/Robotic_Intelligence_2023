from concurrent.futures import ThreadPoolExecutor
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from std_msgs.msg import String


class FilteredSub(Node):

    def __init__(self):
        super().__init__('filtered_sub')
        self.subscription = self.create_subscription(
            Image,
            '/random',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        self.get_logger().info('I heard a message:')
        cv2.imshow("image", self.bridge.imgmsg_to_cv2(msg, "bgr8"))
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = FilteredSub()

    while True:
        get_message = input("Do you want the most recent image? (y/n)")
        if get_message != 'n':
            rclpy.spin_once(minimal_subscriber, timeout_sec=1)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()