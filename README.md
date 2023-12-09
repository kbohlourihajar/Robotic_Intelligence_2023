# Making the map
```ros2 launch slam_toolbox online_async_launch.py```

`rviz2`

`ros2 run teleop_twist_keyboard teleop_twist_keyboard` or `ros2 run turtlebot3_teleop teleop_keyboard`

`ros2 run nav2_map_server map_saver_cli -f ~/map`

# Turtlebot3 Waffle Pi
`ros2 launch turtlebot3_bringup robot.launch.py`

`ros2 run v4l2_camera v4l2_camera_node --ros-args -p image_size:="[640,480]"`

# Laptop/Other Computer
`ros2 launch nav2_bringup bringup_launch.py use_sim_time:=True autostart:=True map:=/{PATH_TO_MAP}/map.yaml`

`ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz`

---

### Get patrol points on map
`ros2 topic echo /clicked_point` Click on publish point in rviz2 and get the points you want to patrol

---

`ros2 run tag patrol_node`

`ros2 run tag tag_node`


## Resources
For setting up turtlebot3 - https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/

### Mapping Guides

https://www.youtube.com/watch?v=QP-cxh8qUJQ

https://medium.com/@thehummingbird/ros-2-mobile-robotics-series-part-2-e8dd6116aacb
