from ultralytics import YOLO
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from std_msgs.msg import Bool


class Tag(Node):
    def __init__(self):
        super().__init__('tag_node')
        self.person_angle = None
        self.patrol_publisher = self.create_publisher(
            Bool,
            'set_patrol_state',
            10
        )
        self.camera_subscriber = self.create_subscription(
            Image,
            'image_raw',
            self.camera_callback,
            10)
        self.bridge = CvBridge()
        self.model = YOLO("yolov8x.pt")
        self.patrolling = False
        self.tagged = False

    def camera_callback(self, frame):
        if self.tagged:
            return
        cv_image = self.bridge.imgmsg_to_cv2(frame, 'bgr8')
        results = self.model.track(source=cv_image, classes=0, persist=True, verbose=False, conf=0.8)

        id = results[0].boxes.id
        conf = results[0].boxes.conf
        if id and conf:
            self.tagged = True
            message = Bool()
            message.data = False
            self.patrol_publisher.publish(message)
            while True:
                cv2.imshow("Tag!", cv_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            self.tagged = False
            cv2.destroyAllWindows()
        elif not self.patrolling:
            self.tagged = False
            message = Bool()
            message.data = True
            self.patrol_publisher.publish(message)


def main(args=None):
   rclpy.init(args=args)
   tag = Tag()
   rclpy.spin(tag)
   tag.destroy_node()