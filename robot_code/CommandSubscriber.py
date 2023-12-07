import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import time
from car import Car
import json


class CommandSubscriber(Node):
    def __init__(self):
        super().__init__('command_listener')
        self.subscription = self.create_subscription(String, '/command', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.car = Car()

    def listener_callback(self, msg):
        self.get_logger().info(f"received command: {msg.data}")
        print(f"received command: {msg.data}")
        command = json.loads(msg.data)
        if command['command'] == 'rotate':
            if command['amount'] < 0:
                self.car.control_car(0, 200)
            else:
                self.car.control_car(200, 0)
            time.sleep(command['amount'])
            self.car.control_car(0, 0)
        elif command['command'] == 'drive':
            self.car.control_car(100, 100)
            time.sleep(command['amount'])
            self.car.control_car(0, 0)
        elif command['command'] == 'search':
            # this part either needs an image pub/sub intermediary on the robot
                # or another way to tell the server to take the results from yolo
            self.car.set_servo(1, 180)
            self.car.set_servo(2, 90)
            time.sleep(0.5)
            self.car.set_servo(1, 144)
            time.sleep(0.5)
            self.car.set_servo(1, 108)
            time.sleep(0.5)
            self.car.set_servo(1, 72)
            time.sleep(0.5)
            self.car.set_servo(1, 36)
            time.sleep(0.5)
            self.car.set_servo(1, 0)
            time.sleep(0.5)
        elif command['command'] == 'ready':
            self.get_logger().info("My body is ready.")

def main(args=None):
    rclpy.init(args=args)

    command_sub = CommandSubscriber()

    rclpy.spin(command_sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    command_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
