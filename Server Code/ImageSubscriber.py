import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
from ultralytics import YOLO

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_saver')
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.model = YOLO("best.onnx")

    def listener_callback(self, msg):
        self.get_logger().info('Received image')
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            # show the image
            cv2.imshow("image", cv2_img)
            cv2.waitKey(1)
            # Predict using the YOLO model
            results = self.model.predict(cv2_img)

            for result in results:
                print(type(result.boxes.cls))
                print(result.boxes.xywh)

def main(args=None):
    rclpy.init(args=args)

    image_saver = ImageSubscriber()

    rclpy.spin(image_saver)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    cv2.destroyAllWindows()
    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()