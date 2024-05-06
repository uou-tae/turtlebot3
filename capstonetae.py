import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
import time

# 초기 로봇의 위치를 저장하는 변수
initial_pose = None
work = 0
gohome = 0 # 초기 gohome 값 0으로 지정
def move_turtlebot3_to_goal(x, y):
    # 목표 위치를 설정한 PoseStamped 메시지 생성
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 0.1)

    # /move_base_simple/goal 토픽에 목표 위치 메시지 발행
    goal_publisher.publish(goal_pose)
    rospy.loginfo("Published goal pose: {}".format(goal_pose))
    

def status_callback(msg):
    global work , gohome
    for status in msg.status_list:
        if status.status == 3  :  # status가 3인 경우  goal reachead 인상태
            work = work + 1      # work 1 씩 증가    
            print(work)
            if work > 50 :
                move_turtlebot3_to_goal(0, 0)  # 첫 번째 실행후 0,0에서 status가 3으로 남아있어서 
                rate.sleep()

def status_subscriber():
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)

if __name__ == "__main__": 
    try:
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        rospy.sleep(1)  # Publisher가 초기화될 때까지 대기
        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed
        move_turtlebot3_to_goal(0.9309288859367371 ,-1.141640067100525)
        rate.sleep()
        print("fitst move goal")

        time.sleep(1) # 첫 번째 동작이후 status가 3이 남아 있다면 도착한걸로 인식하기에 로봇을 보내고 1초 기다림
        status_subscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
