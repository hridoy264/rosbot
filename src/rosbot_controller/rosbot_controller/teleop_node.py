import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TeleopNode(Node):

    def __init__(self):
        super().__init__('teleop_node')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    def run_keyboard(self):
        while rclpy.ok():
            key = input("Enter command: ").strip().lower()

            twist = Twist()

            if key == 'w':
                twist.linear.x = .30

            elif key == 's':
                twist.linear.x = -.30

            elif key == 'a':
                twist.angular.z = .30

            elif key == 'd':
                twist.angular.z = -.30
            
            elif key == 'x':
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            elif key == 'q':
                self.get_logger().info("Quitting teleop node")
                break
            else:
                self.get_logger().info("Invalid key")
                continue
                

            self.publisher.publish(twist)
            self.get_logger().info(
                f"Published: linear.x={twist.linear.x}, angular.z={twist.angular.z}"
            )

def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()

    try:
        node.run_keyboard()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()