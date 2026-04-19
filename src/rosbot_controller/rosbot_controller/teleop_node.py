import sys
import select
import termios
import tty
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
        self.linear_speed = 0.30
        self.angular_speed = 0.30
        self.last_command = None
    def get_key(self):
        """Read one key press without needing Enter."""
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            # Arrow keys come as escape sequence: \x1b [ A/B/C/D
            if key == '\x1b':
                key += sys.stdin.read(2)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key
    def publish_command(self, linear_x=0.0, angular_z=0.0):
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.publisher.publish(twist)
        current = (linear_x, angular_z)
        if current != self.last_command:
            self.get_logger().info(
                f"Published: linear.x={linear_x}, angular.z={angular_z}"
            )
            self.last_command = current
    def run_keyboard(self):
        self.settings = termios.tcgetattr(sys.stdin)
        print("Arrow key teleop started")
        print("↑ = forward, ↓ = backward, ← = left, → = right")
        print("q = quit")
        print("No key = stop")
        try:
            while rclpy.ok():
                key = self.get_key()
                if key == '\x1b[A':      # Up arrow
                    self.publish_command(self.linear_speed, 0.0)
                elif key == '\x1b[B':    # Down arrow
                    self.publish_command(-self.linear_speed, 0.0)
                elif key == '\x1b[D':    # Left arrow
                    self.publish_command(0.0, self.angular_speed)
                elif key == '\x1b[C':    # Right arrow
                    self.publish_command(0.0, -self.angular_speed)
                elif key == 'q':
                    self.publish_command(0.0, 0.0)
                    self.get_logger().info("Quitting teleop node")
                    break
                else:
                    # No key or unknown key -> stop
                    self.publish_command(0.0, 0.0)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        node.run_keyboard()
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_command(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()