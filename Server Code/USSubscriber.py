import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class USSubscriber(Node):

    def __init__(self):
        super().__init__('ultrasonic_subscriber')
        self.sensorFeedback = 420 # initialize it to a far away value that can be easily recognized for debugging
        self.subscription = self.create_subscription(
            Float64,
            '/ultrasonic',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f"I heard: {msg.data}")
        self.sensorFeedback = msg.data

    def getFeedback(self):
        return self.sensorFeedback


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = USSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()