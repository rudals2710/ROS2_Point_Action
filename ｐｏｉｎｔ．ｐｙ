import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import FollowWaypoints

class FollowWaypointsClient(Node):
    def __init__(self):
        # ROS2 노드 초기화
        super().__init__('follow_waypoints_client')

        # Navigation2 Action Client 초기화
        self._action_client = ActionClient(self, FollowWaypoints, 'FollowWaypoints')

      
    def send_goal(self):
        # Navigation2 Action 요청 생성
        print("hello")

        goal_msg = FollowWaypoints.Goal()
        
        pose1 = PoseStamped()
        pose1.header.frame_id='map'
        pose1.pose.position.x = 3.66
        pose1.pose.position.y = 4.04
        pose1.pose.position.z = 0.0
        pose1.pose.orientation.w = 0.03
        pose1.pose.orientation.z = -0.99

        pose2 = PoseStamped()
        pose2.header.frame_id='map'
        pose2.pose.position.x = -0.43
        pose2.pose.position.y = 4.28
        pose2.pose.position.z = 0.0
        pose2.pose.orientation.w =0.03
        pose2.pose.orientation.z =0.99


        goal_msg.poses = [pose1, pose2]

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

    # Wait for the result
        while rclpy.ok():
            status = goal_handle.get_status()
            if status == GoalStatus.STATUS_SUCCEEDED:
                self.get_logger().info('Goal succeeded!')
                break
            elif status == GoalStatus.STATUS_CANCELED:
                self.get_logger().info('Goal canceled')
                break
            elif status == GoalStatus.STATUS_ABORTED:
                self.get_logger().info('Goal aborted')
                break

        # Sleep for a short period of time
            time.sleep(0.1)

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    follow_waypoints_client = FollowWaypointsClient()

    follow_waypoints_client.send_goal()

    rclpy.spin(follow_waypoints_client)


if __name__ == '__main__':
    main()

