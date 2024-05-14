import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math

class Joints(Node):
    def __init__(self):
        super().__init__("talker")
        self.joint_pubs = []  # List to store joint publishers
        self.num_joints = 9  # Number of joints in your snake robot
        self.phase_shift = -40
        self.a = 20.0

        # Create publishers for each joint
        for i in range(self.num_joints):
            topic_name = f"/joints{i + 1}_controllers/commands"
            self.joint_pubs.append(self.create_publisher(Float64MultiArray, topic_name, 10))

        timer_period = 4
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        # Compute desired joint angles (spring-like behavior)
        desired_angles = [self.a * math.sin(self.count + i * self.phase_shift) for i in range(self.num_joints)]

        # Publish desired joint angles
        for i in range(self.num_joints):
            msg = Float64MultiArray()
            msg.data = [desired_angles[i]]
            self.joint_pubs[i].publish(msg)

        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    joint_controller = Joints()
    rclpy.spin(joint_controller)
    joint_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
