#!/usr/bin/python3

import rospy
from actionlib_msgs.msg import GoalStatusArray

def status_callback(msg):
    # 메시지를 처리하는 콜백 함수
    for status in msg.status_list:
        # status_list에 있는 각 status를 처리
        if status.status == 3:  # status가 3인 경우
            rospy.loginfo("ok")  # "ok"를 출력
            print("ok")
            break  # 하나만 출력하고 종료

def status_subscriber():
    rospy.init_node('status_subscriber', anonymous=True)
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)
    rospy.spin()  # 노드가 종료될 때까지 실행 대기

if __name__ == '__main__':
    try:
        status_subscriber()
    except rospy.ROSInterruptException:
        pass
