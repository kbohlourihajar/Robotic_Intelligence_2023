# Overview
This code is to get a the turtlebot3 to play tag. It can patrol around a map you make/provide and looks for a person using its camera to detect them. Once it sees a person it will stop and display tag with the image of who it tagged on the device. To resume the game click 'q' to quit the image and the robot will resume playing tag.

### Demo Patrol in Simulation
![Patrol Simulation](assets/patrol_sim.gif)

### Demo Tag
![Tag](assets/tag_demo.gif)

# How To
You must be on the same local network. You can check with `hostname -I`.

Turtlebot3 code is expected to be run through ssh.

This assumes you have ros2 already running on your computer, we used Humble.

Clone this report and move tag into your ros2 workspaces src directory. Then build it from your workspace:

`colcon build --symlink-install --packages-select tag`

source the install

`source install/setup.bash`

# Exports
Add these to your bashrc or export them per terminal used.

`export TURTLEBOT3_MODEL=waffle_pi`

`export ROS_DOMAIN_ID=30`

# Dependencies
If you are not using Humble for your ros2 distro you can replace the word humble with your distro name.

`sudo apt install ros-humble-slam-toolbox`

`sudo apt install ros-humble-teleop-twist-keyboard`

`sudo apt install ros-humble-navigation2`

`sudo apt install ros-humble-nav2-bringup`

### On the Turtlebot3
`sudo apt install ros-humble-turtlebot3-bringup`

`sudo apt install ros-humble-v4l2-camera`

# Turtlebot3 Waffle Pi
I use tmux to run both of these.

`ros2 launch turtlebot3_bringup robot.launch.py`

`ros2 run v4l2_camera v4l2_camera_node --ros-args -p image_size:="[640,480]"`

# Making the map
Use tmux or open more terminals to run the code.

`rviz2`

```ros2 launch slam_toolbox online_async_launch.py```

In rviz2 add(bottom left) LaserScan (topic /scan), Map (topic /map), TF

`ros2 run turtlebot3_teleop teleop_keyboard`

Once you have it mapped in rviz you can save the map with:

`ros2 run nav2_map_server map_saver_cli -f ~/map`

# Laptop/Other Computer
Use tmux or open more terminals to run the code.

`ros2 launch nav2_bringup bringup_launch.py use_sim_time:=True autostart:=True map:=/{PATH_TO_MAP}/map.yaml`

`ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz`

---

### Get patrol points on map
`ros2 topic echo /clicked_point` Click on publish point in rviz2 and get the points you want to patrol and add them to the bottom of `tag/tag/patrol_node.py`.

---

`ros2 run tag patrol_node`

In rviz2 click on 2D Point Estimator and click where the bot is approximately with dragging the arrow where the robot is facing.

`ros2 run tag tag_node`


## Resources
For setting up turtlebot3 - https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/

### Mapping Guides

https://www.youtube.com/watch?v=QP-cxh8qUJQ

https://medium.com/@thehummingbird/ros-2-mobile-robotics-series-part-2-e8dd6116aacb
