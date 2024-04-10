import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry

# 초기 로봇의 위치를 저장하는 변수
initial_pose = None

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

def odom_callback(msg):
    # 로봇의 초기 위치를 콜백 함수에서 설정
    global initial_pose
    if initial_pose is None:
        initial_pose = msg.pose.pose

if __name__ == "__main__":
    try:
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        rospy.Subscriber("/odom", Odometry, odom_callback)
        rospy.sleep(1)  # Publisher가 초기화될 때까지 대기

        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed

        # 첫 번째 목표 위치로 이동
        move_turtlebot3_to_goal(-0.34728726744651794 ,1.197120189666748)
        rate.sleep()
        
      # 초기 위치로 이동
        move_turtlebot3_to_goal(initial_pose.position.x, initial_pose.position.y)
        rate.sleep()

    except rospy.ROSInterruptException:
        pass
