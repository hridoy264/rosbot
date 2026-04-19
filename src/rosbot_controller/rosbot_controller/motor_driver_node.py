import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import gpiod
from gpiozero import PWMOutputDevice

class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')
        self.MAX_SPEED = 1.2   # 120% max speed
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.motor_callback,
            10
        )

        self.chip = gpiod.Chip('gpiochip4')

        # Direction pins with gpiod
        self.IN1 = self.chip.get_line(17)
        self.IN2 = self.chip.get_line(27)
        self.IN3 = self.chip.get_line(22)
        self.IN4 = self.chip.get_line(23)

        self.IN1.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN2.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN3.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)
        self.IN4.request(consumer="motor_driver", type=gpiod.LINE_REQ_DIR_OUT)

        # PWM speed pins
        self.ENA = PWMOutputDevice(18, frequency=1000)
        self.ENB = PWMOutputDevice(19, frequency=1000)

        self.stop_motors()
        self.get_logger().info('Motor driver node started')

    def stop_motors(self):
        self.ENA.value = 0.0
        self.ENB.value = 0.0
        self.IN1.set_value(0)
        self.IN2.set_value(0)
        self.IN3.set_value(0)
        self.IN4.set_value(0)

    def set_direction(self, left, right):
        # left motor
        if left > 0:
            self.IN1.set_value(0)
            self.IN2.set_value(1)
        elif left < 0:
            self.IN1.set_value(1)
            self.IN2.set_value(0)
        else:
            self.IN1.set_value(0)
            self.IN2.set_value(0)

        # right motor
        if right > 0:
            self.IN3.set_value(0)
            self.IN4.set_value(1)
        elif right < 0:
            self.IN3.set_value(1)
            self.IN4.set_value(0)
        else:
            self.IN3.set_value(0)
            self.IN4.set_value(0)

    def set_speed(self, left_speed, right_speed):
        # clamp between 0 and 1 first
        left_speed = max(0.0, min(1.0, left_speed))
        right_speed = max(0.0, min(1.0, right_speed))

        # apply max speed scaling
        left_speed *= self.MAX_SPEED
        right_speed *= self.MAX_SPEED

        self.ENA.value = left_speed
        self.ENB.value = right_speed
    def motor_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        left = linear-angular
        right = linear+angular

        max_val = max(abs(left), abs(right), 1.0)
        left /= max_val
        right /= max_val

        self.set_direction(left, right)
        self.set_speed(abs(left), abs(right))

    def destroy(self):
        self.stop_motors()
        self.IN1.release()
        self.IN2.release()
        self.IN3.release()
        self.IN4.release()
        self.ENA.close()
        self.ENB.close()

def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()