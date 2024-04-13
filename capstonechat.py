import rospy
from geometry_msgs.msg import PoseStamped, Quaternion
from actionlib_msgs.msg import GoalStatusArray

class TurtlebotController:
    def __init__(self):
        self.goal_positions = [
            (-0.34728726744651794, 1.197120189666748),  # 첫 번째 목표 위치
            (0, 0)  # 두 번째 목표 위치
        ]
        self.current_goal_index = 0  # 현재 목표 위치 인덱스
        self.goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        rospy.Subscriber("/move_base/status", GoalStatusArray, self.status_callback)

    def move_turtlebot3_to_goal(self, x, y):
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = "map"
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.orientation = Quaternion(0.0, 0.0, 0.0, 0.1)

        self.goal_publisher.publish(goal_pose)
        rospy.loginfo("Published goal pose: {}".format(goal_pose))

    def status_callback(self, msg):
        for status in msg.status_list:
            if status.status == 3:  # 목표에 도달한 경우
                if self.current_goal_index == 0:
                    self.current_goal_index = 1
                    self.move_turtlebot3_to_goal(*self.goal_positions[1])
                else:
                    # 두 번째 목표에 도달하여 작업이 완료되었음을 나타냄
                    rospy.signal_shutdown("Mission complete.")

    def run(self):
        rospy.spin()

if __name__ == "__main__":
    rospy.init_node("turtlebot_controller")
    try:
        controller = TurtlebotController()
        controller.move_turtlebot3_to_goal(*controller.goal_positions[0])  # 초기 위치로 이동
        controller.run()
    except rospy.ROSInterruptException:
        pass
