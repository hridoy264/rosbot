import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Vector3 


class CmdVelNode(Node):

    def __init__(self):

        super().__init__('cmd_vel_node')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.motor_publisher = self.create_publisher(
            Vector3,
            '/motor_cmd',
            10
        )

        self.get_logger().info('CmdVelNode started. Listening on /cmd_vel')
        self.get_logger().info('Subscribed to /cmd_vel')
        self.get_logger().info('Publishing motor commands to /motor_cmd')


    def cmd_vel_callback(self, msg: Twist):

        linear_x = msg.linear.x
        angular_z = msg.angular.z

        left_motor = linear_x - angular_z 
        right_motor = linear_x + angular_z 

        motor_msg = Vector3()
        motor_msg.x = left_motor
        motor_msg.y = right_motor
        motor_msg.z = 0.0

        self.motor_publisher.publish(motor_msg)

        self.get_logger().info(
            f'Received cmd_vel -> linear.x: {linear_x}, angular.z: {angular_z}'
        )
        self.get_logger().info(
            f'Computed motor speeds -> left: {left_motor}, right: {right_motor}'
        )

def main(args=None):
    rclpy.init(args=args)
    node=CmdVelNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()