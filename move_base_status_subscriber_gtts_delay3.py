#!/usr/bin/python3

import rospy
from actionlib_msgs.msg import GoalStatusArray
#pip install gtts ==1.2.2
#pip install playsound 위 두 문장 해줘야함
from gtts import gTTS
from playsound import playsound

def status_callback(msg):
    # 메시지를 처리하는 콜백 함수
    for status in msg.status_list:
        # status_list에 있는 각 status를 처리
        if status.status == 3:  # status가 3인 경우
            print("ok")
        if status.status == 1 :
            print("working")

            #gtts 사운드 재생
            audio = 'speech.mp3'
            language = 'ko'

            sp = gTTS(
            lang=language,
            text="운행중입니다",
            slow=False
            )

            time.sleep(3)  #3초 대기 후 다시 출력
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
