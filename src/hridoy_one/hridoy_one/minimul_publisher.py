import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimulPublisher(Node):
    def __init__(self):
        super().__init__('minimul_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello world %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
def main(args=None):
    rclpy.init(args = args)

    minimul_publisher = MinimulPublisher()
    rclpy.spin(minimul_publisher)
    minimul_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()