import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotorDriver(Node):

    def __init__(self):
        super().__init__('motor_driver')

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_callback,
            10
        )
    
    def cmd_callback(self, msg):

        linear = msg.linear.x
        angular = msg.angular.z

        self.get_logger().info(f'Linear:{linear} Angular: {angular}')

def main(args = None):
    rclpy.init(args=args)
    node = MotorDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()