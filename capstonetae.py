import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray

# 초기 로봇의 위치를 저장하는 변수
initial_pose = None
work = 0
gohome = 0
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
        if status.status == 3:  # status가 3인 경우  goal reachead 인상태
            work = work + 1      # work 1 씩 증가    
            if gohome == 1 :
                rospy.signal_shutdown("Mission complete.")

def status_subscriber():
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)

if __name__ == "__main__":
    try:
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        status_subscriber()

        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed
        if work == 0:
            # 첫 번째 동작 목표 위치로 이동
            move_turtlebot3_to_goal(-0.34728726744651794 ,1.197120189666748)
        elif work > 100:
            # 두 번째 동작 초기 위치로 이동
            move_turtlebot3_to_goal(0, 0)
            gohome = 1


        rate.sleep()
        
        
        
    except rospy.ROSInterruptException:
        pass
