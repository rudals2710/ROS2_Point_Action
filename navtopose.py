import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import time
class MapNAvigation(Node):

  def __init__(self):
    super().__init__('map_navigation')
    self.get_logger().info("Press Ctrl-C to stop the node...")

    #315,310,323,324
    self.xone_five=15.50
    self.yone_five=15.50
    self.xone_zero=10.20
    self.yone_zero=10.20
    self.xtwo_three=27.70
    self.ytwo_three=27.70
    self.xtwo_four=30.44
    self.ytwo_four=30.44

    self.get_logger().info('Waiting for action server...')
    self._action_client=ActionClient(self, NavigateToPose,'navigate_to_pose')

    if not self.client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available')
            self.destroy_node()
            exit(0)
    
    choice = self.choose()

    while choice != 'q':
        if choice == '0':
            self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)
        elif choice == '1':
            self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)
        elif choice == '2':
            self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)
        elif choice == '3':
            self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)

        if choice != 'q':
            if self.goalReached:
                self.get_logger().info('Congratulations!')
            else:
                self.get_logger().info('Hard Luck!')
                    
    

  def goal_callback(self,msg):
     goal=NavigateToPose.Goal()
     goal.pose=msg #필요한지 잘 모르겠음

     self._action_client.wait_for_result()
     self._action_client.send_goal(goal)
     while not self._action_client.wait_for_result():
            pass

     if self._action_client.get_result().result == 0:
         self.get_logger().info('Congratulations!')
     else:
         self.get_logger().info('Hard Luck!')

  def shutdown(self):
      #stop robot
      self.get_logger().info('Quit program')
      self.client.destroy_node()
      rclpy.shutdown()

  def choose(self):
        choice = 'q'

        self.get_logger().info("|-------------------------------|")
        self.get_logger().info("|PRESSE A KEY:")
        self.get_logger().info("|'0': 310 ")
        self.get_logger().info("|'1': 315")
        self.get_logger().info("|'2': 323 ")
        self.get_logger().info("|'3': 324 ")
        self.get_logger().info("|'q': Quit ")
        self.get_logger().info("|-------------------------------|")
        self.get_logger().info("|WHERE TO GO?")
        choice = input()

        return choice
  
  def moveToCoal(self,xGoal,yGoal):
        goal_msg = NavigateToPose.Goal()
        
        pose1 = PoseStamped()

        pose1.header.frame_id='map'
        pose1.poses.pose.position.x = 0.0
        pose1.pose.position.y = 0.0
        pose1.pose.position.z = 0.0
        pose1.pose.orientation.w = 0.0
        pose1.pose.orientation.z = 0.0

        goal_msg.pose=pose1

        self.get_logger().info('Sending goal location...')
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)


def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
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
    map_navigation = MapNAvigation()
    map_navigation.send_goal()
    rclpy.spin(map_navigation)

if __name__ == '__main__':
    main()
