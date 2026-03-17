import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotorDriver(Node):
    def __init__(self):
        super().__init__('motor_driver')

        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        
    def cmd_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        if linear > 0:
            self.get_logger().info("Forward")

        elif angular > 0:
            self.get_logger.info("Left")

        elif angular < 0:
            self.get_logger().info("Right")

        else:
            self.get_logger().info("Stop")

    
def main(args=None):
    rclpy.init(args=args)

    node = MotorDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()