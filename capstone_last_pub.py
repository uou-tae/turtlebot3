import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
import time

# 초기 로봇의 위치를 저장하는 변수
initial_pose = None
work = 0
gohome = 0 # 초기 gohome 값 0으로 지정
goal_index = 0
goals = [
    (0.8643271923065186, -0.2915951609611511, Quaternion(0.0, 0.0,  -0.7145780324935913,0.6995557546615601)),
    (0.5380954742431641,-0.676059365272522, Quaternion(0.0, 0.0, -0.9248950481414795, 0.38022252917289734)),
    (0.3650090992450714, -1.0044853687286377, Quaternion(0.0, 0.0,-0.7324463129043579, 0.6808247566223145)),
    (0.9600212574005127,-1.1722830533981323, Quaternion(0.0, 0.0, 0.01755490154027939,  0.9998459219932556)),
    (0.4146745800971985, -0.9552727937698364, Quaternion(0.0, 0.0, 0.6694647073745728 , 0.7428438663482666)),
    (0.6452376842498779, -0.5942646861076355, Quaternion(0.0, 0.0, 0.42138510942459106, 0.9068818092346191)),
    (0.850282609462738, -0.20427416265010834, Quaternion(0.0, 0.0, 0.7040437459945679, 0.7101566195487976)),
    (0.0, 0.0, Quaternion(0.0, 0.0, -0.9999961256980896, -0.0027858419343829155))
]

def move_turtlebot3_to_goal(x, y, orientation):
    
        
        # Create a PoseStamped message for the goal position
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = "map"
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.orientation = orientation

        # Publish the goal pose
        goal_publisher.publish(goal_pose)
        rospy.loginfo("Published goal pose: {}".format(goal_pose))
    

def status_callbacked(msg):
    global goal, work
    for status in msg.status_list:
        if status.status == 0:  # status가 0인 경우
            print("callback Status: ", status.status)


def status_callback(msg):
    global work , gohome, goal_index
    msg = rospy.wait_for_message("/move_base/status", GoalStatusArray)
    for status in msg.status_list:
        if status.status == 3  :  # status가 3인 경우  goal reachead 인상태
            work = work + 1      # work 1 씩 증가    
            print(work)
            if goal_index == 3:
                if work > 50 :
                    goal_index = goal_index + 1
                    x, y, orientation = goals[goal_index]
                    move_turtlebot3_to_goal(x, y, orientation) # 첫 번째 실행후 0,0에서 status가 3으로 남아있어서 
                    rate.sleep()
                    work = 0
                #추가된 부분
                elif work == 10 :
                    pub.publish(1)


            if goal_index !=3 :
                if work > 5 :
                    goal_index = goal_index + 1
                    x, y, orientation = goals[goal_index]
                    move_turtlebot3_to_goal(x, y, orientation) # 첫 번째 실행후 0,0에서 status가 3으로 남아있어서 
                    rate.sleep()
                    work = 0
            

        if status.status == 1:
            work = 0


def status_subscriber():
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callbacked)

if __name__ == "__main__": 
    try:
        goal_index = 0
        x, y, orientation = goals[goal_index]
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)

        pub = rospy.Publisher('goal_reached', int, queue_size=10)

        rospy.sleep(1)  # Publisher가 초기화될 때까지 대기
        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed
        move_turtlebot3_to_goal(x, y, orientation)
        rate.sleep()
        print("fitst move goal")

        time.sleep(1) # 첫 번째 동작이후 status가 3이 남아 있다면 도착한걸로 인식하기에 로봇을 보내고 1초 기다림
        status_subscriber()
        rospy.Timer(rospy.Duration(0.1), status_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
