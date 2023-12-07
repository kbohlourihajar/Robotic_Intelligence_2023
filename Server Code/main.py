from BotCommands import BotCommands
import rclpy

bot_commands = BotCommands()

bot_commands.sendMessage()

def main(args=None):
    # start up the following nodes
        # Server:
            # CommandPublisher
            # ImageSubscriber
            # UltrasonicSubscriber
            # 
        # Robot:
            # Camera -> $ ros2 run v4l2_camera v4l2_camera_node --ros-args -p image_size:="[640,480]"
            # CommandSubscriber
            # UltrasonicPublisher
            # 
            
    # process for moving one ball to the goal
        # loop until the robot is pointed at the ball
            # tell the robot to scan for the ball
            # calculate the angle of the ball relative to the robot
            # tell the robot to rotate to face the ball

        # loop until the ultrasonic sensor indicates that the ball is in the catcher
            # tell the robot to scan for the ball
            # calculate the distance to the ball
            # tell the robot to drive forward that distance
        
        # loop until the robot is pointed at the goal
            # tell the robot to scan for the goal
            # calculate the angle of the goal relative to the robot
            # tell the robot to rotate to face the goal
        
        # loop until the robot is close enough to the goal
            # tell the robot to scan for the goal
            # calculate the distance to the goal
            # tell the robot to drive forward that distance
        
        # tell the robot to back up and turn around (set up to perform the ball process again)

    rclpy.init(args=args)

    minimal_publisher = CommandPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()