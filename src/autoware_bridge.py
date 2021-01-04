#!/usr/bin/env python
import rospy
from autoware_msgs.msg import VehicleCmd
from std_msgs.msg import Int16MultiArray


linear_velocity = 0
steer_angle = 0
brake_value = 0
max_steering_angle = 30
steering_unit = 1024/max_steering_angle


pub = rospy.Publisher('/control_cmd', Int16MultiArray, queue_size=1)

max_acc = 20

def callback(data):
    linear_velocity = int(data.ctrl_cmd.linear_velocity*36)
    steer_angle = -int(data.ctrl_cmd.steering_angle*57.30*steering_unit)
    brake_value = int(data.ctrl_cmd.linear_acceleration*1000/max_acc)
    if brake_value > 0:
        brake_value = 0
    elif brake_value < -1024:
        brake_value = 1024
    if linear_velocity > 600:
        linear_velocity = 600
    if steer_angle > 1024:
        steer_angle = 1024
    elif steer_angle < -1024:
        steer_angle = -1024

    msg = Int16MultiArray(data=[linear_velocity, steer_angle, -brake_value, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]) 
    rospy.loginfo(msg.data)
    pub.publish(msg)



def listener():
    rospy.init_node('autoware_bridge', anonymous=True)
    rospy.Subscriber('/vehicle_cmd', VehicleCmd, callback)
    rospy.spin()


if __name__ == "__main__":
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
