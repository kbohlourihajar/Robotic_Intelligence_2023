import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from std_msgs.msg import Bool


class Patrol(Node):

    def __init__(self, patrol_points):
        super().__init__('autonomy_node')
        self.patrol_points = patrol_points
        self.navigator = BasicNavigator()
        self.patrolling = False
        self.patrol_index = 0
        self.navigator.waitUntilNav2Active()
        self.goal = PoseStamped()
        self.patrol_service = self.create_subscription(Bool, 'set_patrol_state', self.handle_patrol_callback, 10)
        self.patrol_timer = self.create_timer(0.5, self.patrol_callback)  # Adjust the timer period as needed
    
    def handle_patrol_callback(self, msg):
        self.patrolling = msg.data
        if not self.patrolling:
            self.navigator.cancelTask()
            self.patrol_index = self.patrol_index if self.patrol_index - 1 < 0 else self.patrol_index - 1 

    def patrol_callback(self):
        if not self.patrolling:
            return  # Do nothing if not patrolling

        if self.navigator.isTaskComplete():
            if self.patrol_index >= len(self.patrol_points):
                self.patrol_index = 0  # Reset to the first point

            x, y, theta = self.patrol_points[self.patrol_index]
            self.set_goal(x, y, theta)
            self.navigator.goToPose(self.goal)
            self.patrol_index += 1  # Move to the next goal
    
    def set_goal(self, x, y, w):
        self.goal.header.stamp = self.get_clock().now().to_msg()
        self.goal.header.frame_id = "map"
        self.goal.pose.position.x = x
        self.goal.pose.position.y = y
        self.goal.pose.orientation.z = w


def main(args=None):
    rclpy.init(args=args)

    # set these based on your map
    patrol_points = [
            (-0.7012170553207397, 1.0324088335037231, 0.101959228515625),
            (-0.42683398723602295, -1.1036051511764526, -0.001373291015625),
            (3.018293619155884, -1.0731033086776733, -0.001434326171875), 
            (2.9878149032592773, 1.2765108346939087, -0.001434326171875), 

        ]

    autonomy_publisher = Patrol(patrol_points)

    rclpy.spin(autonomy_publisher)
    autonomy_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()