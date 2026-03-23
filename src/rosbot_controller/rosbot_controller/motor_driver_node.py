import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
import gpiod

class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')

        self.subscription = self.create_subscription(
            Vector3,
            '/motor_cmd',
            self.motor_callback,
            10
        )

        #Raspberry Pi 5 GPIO chip
        self.chip = gpiod.Chip('gpiochip4')

        self.IN1 = self.chip.get_line(17)
        self.ENA = self.chip.get_line(18)
        self.IN2 = self.chip.get_line(27)
        self.IN3 = self.chip.get_line(22)
        self.IN4 = self.chip.get_line(23)
        self.ENB = self.chip.get_line(19)

        #Request all as outputs
        self.IN1.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN2.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.ENA.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN3.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN4.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.ENB.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)


        self.stop_motors()
        self.get_logger().info('Motor driver node started with gpiod')

    def stop_motors(self):
        self.ENA.set_value(0)
        self.ENB.set_value(0)
        self.IN1.set_value(0)
        self.IN2.set_value(0)
        self.IN3.set_value(0)
        self.IN4.set_value(0)

    def move_forward(self):
        self.ENA.set_value(1)
        self.ENB.set_value(1)

        self.IN1.set_value(0)
        self.IN2.set_value(1)

        self.IN3.set_value(0)
        self.IN4.set_value(1)

    def move_backward(self):
        self.ENA.set_value(1)
        self.ENB.set_value(1)

        self.IN1.set_value(1)
        self.IN2.set_value(0)

        self.IN3.set_value(1)
        self.IN4.set_value(0)

    def turn_left(self):
        self.ENA.set_value(1)
        self.ENB.set_value(1)

        self.IN1.set_value(1)
        self.IN2.set_value(0)

        self.IN3.set_value(0)
        self.IN4.set_value(1)

    def turn_right(self):
        self.ENA.set_value(1)
        self.ENB.set_value(1)

        self.IN1.set_value(0)
        self.IN2.set_value(1)

        self.IN3.set_value(1)
        self.IN4.set_value(0)

    def motor_callback(self, msg):
        left = msg.x
        right = msg.y

        self.get_logger().info(f'Received motor command: left={left}, right={right}')

        # stop
        if left == 0.0 and right == 0.0:
            self.stop_motors()

        # forward
        elif left > 0 and right > 0:
            self.move_forward()

        # backward
        elif left < 0 and right < 0:
            self.move_backward()

        # turn left
        elif left < right:
            self.turn_left()

        # turn right
        elif left > right:
            self.turn_right()

        else:
            self.stop_motors()


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_motors()
        node.IN1.release()
        node.ENA.release()
        node.IN2.release()
        node.IN3.release()
        node.IN4.release()
        node.ENB.release()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 