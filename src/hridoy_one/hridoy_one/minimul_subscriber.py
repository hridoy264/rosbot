import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimulSubscriber(Node):
    def __init__(self):
        super().__init__("minimul_subscriber")
        self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 10)
        self.subscription
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args = None):
    rclpy.init(args=args)
    minimul_subsrciber = MinimulSubscriber()
    rclpy.spin(minimul_subsrciber)
    minimul_subsrciber.destroy_node()
    rclpy.shutdown()

if(__name__=='__main__'):
    main()
