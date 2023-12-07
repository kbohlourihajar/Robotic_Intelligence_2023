from BotCommands import BotCommands
import rclpy

bot_commands = BotCommands()

bot_commands.sendMessage()

def main(args=None):
    rclpy.init(args=args)
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

    # rotate towards ball
    ball_angle = bot_commands.checkYOLOandUltrasonic()['ball']['angle']
    angle_margin = 2
    forward_angle = 90 # 90 is the forward angle of the camera servo
    while forward_angle - angle_margin < ball_angle < forward_angle + angle_margin:
        ball_angle = bot_commands.checkYOLOandUltrasonic()['ball']['angle']
        bot_commands.rotateBot(ball_angle)

    # move to ball
    ball_distance = bot_commands.checkYOLOandUltrasonic()['ball']['distance']
    dist_threshold = 5
    while ball_distance < dist_threshold:
        ball_distance = bot_commands.checkYOLOandUltrasonic()['ball']['distance']
        bot_commands.driveBot(ball_distance)
    
    # rotate to goal
    goal_angle = bot_commands.checkYOLOandUltrasonic()['goal']['angle']
    angle_margin = 2
    forward_angle = 90 # 90 is the forward angle of the camera servo
    while forward_angle - angle_margin < goal_angle < forward_angle + angle_margin:
        goal_angle = bot_commands.checkYOLOandUltrasonic()['goal']['angle']
        bot_commands.rotateBot(ball_angle)
    
    # move to goal
    goal_distance = bot_commands.checkYOLOandUltrasonic()['goal']['distance']
    dist_threshold = 5
    while goal_distance < dist_threshold:
        goal_distance = bot_commands.checkYOLOandUltrasonic()['goal']['distance']
        bot_commands.driveBot(goal_distance)
    
    # tell the robot to back up and turn around (set up to perform the ball process again)
    bot_commands.driveBot(-10)
    # Destroy all the nodes

    rclpy.shutdown()


if __name__ == '__main__':
    main()