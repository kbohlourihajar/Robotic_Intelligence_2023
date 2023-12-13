BotCommands.py - handles robot server interfacing\
CommandPublisher.py - ROS2 publisher node for robot commands\
ImageSubscriber.py - ROS2 subscriber node for robot camera feed\
Server.py - main robot process, ONLY file that needs to be run on the server\
USSubscriber.py - ROS2 subscriber node for robot ultrasonic distance readings\
best.omnx - The YOLOv8 Model we made\
yolo.py - has a function that takes a cv2 image, processes it through yolo and returns positional and classification information.\
