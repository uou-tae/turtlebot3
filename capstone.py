import rospy
from geometry_msgs.msg import PoseStamped, Quaternion


def move_turtlebot3_to_goal(x, y):
    # 목표 위치를 설정한 PoseStamped 메시지 생성
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.orientation = Quaternion(0.0,0.0,0.0,0.1)

    # /move_base_simple/goal 토픽에 목표 위치 메시지 발행
    goal_publisher.publish(goal_pose)
    rospy.loginfo("Published goal pose: {}".format(goal_pose))

if __name__ == "__main__":
    try:
        rospy.init_node("SRL_targetpoint")
        goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        rospy.sleep(1)  # Publisher가 초기화될 때까지 대기

        rate = rospy.Rate(1)  # 1Hz, adjust the rate as needed
        while not rospy.is_shutdown():
            # 원하는 목표 위치로 TurtleBot3 이동 명령 반복적으-0.8로 발행
            move_turtlebot3_to_goal(-3.7371699810028076, -8.3065098520324707)
            
            rate.sleep()

    except rospy.ROSInterruptException:
        pass

