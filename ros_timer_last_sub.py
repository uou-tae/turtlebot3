#!/usr/bin/python3
import rospy
import time
from actionlib_msgs.msg import GoalStatusArray
from playsound import playsound

audio = 'speech.mp3'
audio1 = 'goalreached.mp3'
goal=0
work=0

def status_callback(msg):
    global goal, work
    for status in msg.status_list:
        if status.status == 0:  # status가 0인 경우
            print("callback Status: ", status.status)

def check_status(event):
    # 이제는 TimerEvent 인스턴스 대신에 GoalStatusArray 메시지를 사용함
    global goal, work
    msg = rospy.wait_for_message("/move_base/status", GoalStatusArray)
    for status in msg.status_list:
        if status.status == 3:  # status가 3인 경우
            # print("goal reached")
            print("Status: ", status.status)
            goal += 1
            print(f"goal: {goal}")
            if goal == 30: # goal이 1이면 즉 도착하면 도착하였습니다.
                playsound(audio1)

        if status.status == 1:
            print("working")
            print("Status: ", status.status)
            goal = 0
            work += 1
            print(f"work: {work}")
            if work > 30 : # work 가 3번 이상 즉 3초 유지되면 주행중입니다
                playsound(audio)
                work = 0

def callback(data): # 위에 status 3인 경우를 빼야함.
    print(data)
    playsound(audio1) # 도착 하였습니다.


def status_subscriber():
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)

if __name__ == '__main__':
    try:
        rospy.init_node('ros_timer')
        status_subscriber() # status 값을 구독은 계속함
        rospy.Subscriber('goal_reached', int, callback)
        rospy.Timer(rospy.Duration(0.1), check_status) # 1초마다 status 값 조건에 비교함
        rospy.spin()

    except rospy.ROSInterruptException:
        pass