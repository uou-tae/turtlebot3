#!/usr/bin/python3

#pip install playsound 해줘야함

import rospy
import time
from actionlib_msgs.msg import GoalStatusArray
from playsound import playsound

 audio = 'speech.mp3'

def status_callback(msg):
    # 메시지를 처리하는 콜백 함수
    for status in msg.status_list:
        # status_list에 있는 각 status를 처리
        if status.status == 3:  # status가 3인 경우
            print("goal reached")
            print("Status: ", status.status)
        if status.status == 1 :
            print("working")
            print("Status: ", status.status)
            playsound(audio)
            break  # 하나만 출력하고 종료

def status_subscriber():
    rospy.init_node('status_subscriber', anonymous=True)
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)
    rate = rospy.Rate(0.33)  # 3초에 한 번씩 메시지 처리
    while not rospy.is_shutdown():
        rospy.spinOnce()
        try:
            rate.sleep()
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            pass

if __name__ == '__main__':
    try:
        status_subscriber()
    except rospy.ROSInterruptException:
        pass
