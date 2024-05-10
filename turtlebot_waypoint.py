import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
import time
import math

# 초기 로봇의 위치를 저장하는 변수
initial_pose = None
work = 0
gohome = 0 # 초기 gohome 값 0으로 지정
i = 0
goal = [[0,0], 
        [0.8796108961105347, -0.2965037524700165], 
        [0.5096224546432495,-0.8996579051017761],  
        [0.889918863773346, -1.1491609811782837], 
        [0.3, -1.0], 
        [0.7, -0.6], 
        [0.99, -0.04], 
        [0,0]]
Quaternion = [(0.0, 0.0, 0.0, 0.1),
              Quaternion(0.0, 0.0,  0.6619901061058044, -0.7495126128196716),
              Quaternion(0.0, 0.0, 0.6376864314079285, -0.770296037197113), 
              Quaternion(0.0, 0.0, 0.21, 0.97), 
              Quaternion(0.0, 0.0, -0.0145773496478796, 0.9998937249183655), 
              Quaternion(0.0, 0.0, 0.7960116267204285,-0.6052812933921814),
              Quaternion(0.0, 0.0, 0.025252757593989372, 0.9996811151504517),
              Quaternion(0.0, 0.0, 0.2, 0.1)]

def calculate_rms(x,y):    
    rms = math.sqrt(x**2 + y**2)
    return rms

def move_turtlebot3_to_goal(x, y, z):
    # 목표 위치를 설정한 PoseStamped 메시지 생성
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.orientation = z

    # /move_base_simple/goal 토픽에 목표 위치 메시지 발행
    goal_publisher.publish(goal_pose)
    rospy.loginfo("Published goal pose: {}".format(goal_pose))
    

def status_callback(msg):
    global work , gohome , i
    for status in msg.status_list:
        if status.status == 3  :  # status가 3인 경우  goal reachead 인상태
            work = work + 1      # work 1 씩 증가    
            print(work)
            if work > 30 :
                i=i+1
                move_turtlebot3_to_goal(goal[i][0], goal[i][1], Quaternion[i])  # 첫 번째 실행후 0,0에서 status가 3으로 남아있어서
                rate.sleep()
                work = 0

def status_subscriber():
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)

def odom_callback(msg):
    # 로봇의 초기 위치를 콜백 함수에서 설정
    global i
    current_x = msg.pose.pose.position.x
    current_y = msg.pose.pose.position.y
    goal_distance_x = goal[i][0] - current_x
    goal_distance_y = goal[i][1] - current_y

    result = calculate_rms(goal_distance_x, goal_distance_y)
    if (i != 3):
        if result < 0.1 :
            x = 1
            i = i + 1
            move_turtlebot3_to_goal(goal[i][0] ,goal[i][1], Quaternion[i])
            rate.sleep()
            time.sleep(1) # 첫 번째 동작이후 status가 3이 남아 있다면 도착한걸로 인식하기에 로봇을 보내고 1초 기다림
                

if __name__ == "__main__": 
    try:
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        rospy.sleep(1)  # Publisher가 초기화될 때까지 대기
        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed
        status_subscriber()
        rospy.Subscriber("/odom", Odometry, odom_callback)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
