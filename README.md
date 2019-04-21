# Open Zeka MARC Autonomous Car Base Software

For starting the car:
```bash
source /opt/ros/melodic/setup.bash
# If you are using zsh
# source /opt/ros/melodic/setup.zsh
roslaunch racecar teleop.launch
```

This will initialize all nodes. If you encountered an error, please look at the Troubleshooting section. 

For collecting data:
```bash
rosrun deep_learning collect_data.py
```

The data will be saved on /data folder inside of the deep_learning package. You should have training_data.npy file inside the /data folder. This file contains all of the images name and associated speed and angle. 

For driving autonomously:
```bash
rosrun deep_learning predict.py
```

Note that in order to run these nodes, python3 is required. You need to rebuild cv_bridge package for python3. 

Follow these steps: [cv_bridge for python3](https://github.com/openzeka/cv_bridge_python3)

Tested on Jetson TX2 with Jetpack 4.2 

# Troubleshooting

## ERROR: cannot launch node of type [joy/joy_node]: joy

```bash
ERROR: cannot launch node of type [joy/joy_node]: joy
ROS path [0]=/opt/ros/melodic/share/ros
ROS path [1]=/home/o/cv_bridge_python3/install/share
ROS path [2]=/home/o/openzeka-marc/src
ROS path [3]=/opt/ros/melodic/share
```

You need to install joy packages for ROS
```bash
sudo apt install ros-melodic-joy
```

## ERROR: cannot launch node of type [joy_teleop/joy_teleop.py]: joy_teleop

```bash
ERROR: cannot launch node of type [joy/joy_node]: joy
ROS path [0]=/opt/ros/melodic/share/ros
ROS path [1]=/home/o/cv_bridge_python3/install/share
ROS path [2]=/home/o/openzeka-marc/src
ROS path [3]=/opt/ros/melodic/share
```

You need to install joy-teleop packages for ROS
```bash
sudo apt install ros-melodic-joy-teleop
```

## [FATAL] [1555886343.135289179]: Failed to connect to the VESC, SerialException Failed to open the serial port to the VESC. IO Exception (2): No such file or directory, file /tmp/binarydeb/ros-melodic-serial-1.2.1/src/impl/unix.cc, line 151. failed..

1. First, you should ensure that VESC is correctly plugged in to USB hub. Check with the lsusb command. You should see **STMElectronics** as an output of lsusb. If not, you may try to change the cable. 

2. You should control the VESC battery level. If the VESC blinking the red light, the battery might have drained. 

3. If everything look okay, you may need to set the file write permissions for the VESC. In order to set the full permission for the VESC:
```bash
sudo chmod 777 /dev/ttyACM1
```

4. If nothings mentioned above works, then you need to check the VESC from BLDC-Tool if it is broken or not.  

## [ERROR] [1555886343.178004538]: Error, cannot bind to the specified serial port /dev/ttyUSB0.

1. This error is related to the **RPLidar**. Be sure that RPlidar USB cable is correctly plugged in to USB HUB. 

2. If you sure rplidar is correctly plugged, then you may need to set the file permission for the RPlidar. 
```bash
sudo chmod 777 /dev/ttyACM0
```
## [rplidarNode-14] process has died [pid 2920, exit code 255, cmd /home/o/openzeka-marc/devel/lib/rplidar_ros/rplidarNode __name:=rplidarNode __log:=/home/o/.ros/log/3ebf8f14-6478-11e9-b9d3-0e2c2f0bf36d/rplidarNode-14.log].

This error is also related with the RPLidar. See the previous suggested methods. 

## ** Opening Camera. Attempt 0 ...

1. This means that ZED Camera can not to be seen from the Ubuntu. Make sure that you connect ZED Camera properly to the USB Hub. 

2. This error is also related the power. ZED Camera might not get the required power it's need. Connect the ZED Camera directly the Jetson USB3.0 port and check.


