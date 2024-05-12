import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

class SnakeRobotController(Node):
    def __init__(self, inertia_properties):
        super().__init__('snake_robot_controller')
        self.inertia_properties = inertia_properties
        self.initial_joint_angles = {}
        self.effort_required = {}
        self.joint_publishers = {}

        self.joint_states_subscriber = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_states_callback,
            10
        )
        self.setup_joint_publishers()
        self.calculate_effort_for_each_joint()
        



    def calculate_torque_for_angle(self, link_name, angle_deg):
        print(f"Info: Function calculate_torque_for_angle")
        DEG_TO_RAD = math.pi / 180.0
        if link_name not in self.inertia_properties:
            self.get_logger().error(f"Error: Link '{link_name}' not found in inertia properties.")
            print(f"Error: Link '{link_name}' not found in inertia properties.")
            return None
        angle_rad = angle_deg * DEG_TO_RAD
        link_inertia = self.inertia_properties[link_name]
        mass = link_inertia['mass']
        ixx = link_inertia['ixx']
        iyy = link_inertia['iyy']
        izz = link_inertia['izz']
        torque = (mass * math.pow(angle_rad, 2) + ixx * angle_rad) / math.sin(angle_rad)
        return torque

    def calculate_effort_for_joint(self, joint_name, target_angle_deg):
        print(f"Info: Function calculate_effort_for_joint")
        if joint_name not in self.initial_joint_angles:
            self.get_logger().error(f"Error: Joint '{joint_name}' not found in initial joint angles.")
            print(f"Error: Joint '{joint_name}' not found in initial joint angles.")
            return None
        initial_angle_deg = self.initial_joint_angles[joint_name]
        angle_diff_deg = abs(target_angle_deg - initial_angle_deg)
        effort_required = self.calculate_torque_for_angle(joint_name, angle_diff_deg)
        if effort_required is not None:
            self.effort_required[joint_name] = effort_required
            self.get_logger().info(f"Effort required to move {joint_name} by {angle_diff_deg} degrees: {effort_required} Nm")
            print(f"Effort required to move {joint_name} by {angle_diff_deg} degrees: {effort_required} Nm")
            return effort_required

    def calculate_effort_for_each_joint(self):
        print(f"Info: Function calculate_effort_for_each_joint")
        for joint_name in self.initial_joint_angles:
            self.calculate_effort_for_joint(joint_name, 1.0)  # Calculate effort for moving each joint to 1 degree

    def setup_joint_publishers(self):
        print(f"Info: Function setup_joint_publishers")
        for i in range(len(self.initial_joint_angles)):  # Assuming joints are numbered from 2 to 9
            topic_name = f'/joints{i+1}_controllers/commands'
            self.joint_publishers[self.initial_joint_angles[i]] = self.create_publisher(Float64, topic_name, 10)
            print(f"Info: Joint {self.initial_joint_angles[i]} publisher has been assign by topic name {topic_name} ")

        
        #for joint_name in self.initial_joint_angles:
            #topic_name = f"{joint_name}_controller/command"
            #self.joint_publishers[joint_name] = self.create_publisher(Float64, topic_name, 10)

    def restore_joint_angle(self, joint_name, current_angle):
        print(f"Info: Function restore_joint_angle")
        if joint_name not in self.initial_joint_angles:
            self.get_logger().error(f"Error: Joint '{joint_name}' not found in initial joint angles.")
            print(f"Error: Joint '{joint_name}' not found in initial joint angles.")
            return
        initial_angle = self.initial_joint_angles[joint_name]
        print(f"Recorded current angle of {joint_name}: {current_angle} radians. Restoring to initial angle.")
        angle_diff = current_angle - initial_angle

        effort_to_restore = self.effort_required[joint_name] * angle_diff
        print(f"Effort needed {effort_to_restore}")
        self.send_effort_command(joint_name, effort_to_restore)
        self.get_logger().info(f"Restoring {joint_name} to its initial angle: {initial_angle} radians with an effort of {effort_to_restore} Nm.")
        print(f"Restoring {joint_name} to its initial angle: {initial_angle} radians with an effort of {effort_to_restore} Nm.")


    def send_effort_command(self, joint_name, effort):
        print(f"Info: Function send_effort_command")
        topic_name = f"{joint_name}_controller/command"
        publisher = self.joint_publishers[joint_name]
        msg = Float64()
        msg.data = effort
        publisher.publish(msg)

    def joint_states_callback(self, msg):
            # Check if there is a message in the queue
        print(f"Info: Function joint_states_callback")
        if msg is not None:
            # If the map with initial values of joint angles is empty, fill it with the details in the received message
            if not self.initial_joint_angles:
                for i in range(len(msg.name)):
                    joint_name = msg.name[i]
                    self.initial_joint_angles[joint_name] = msg.position[i]
                    print(f"Info: Joint '{joint_name}' added to initial joint angles with position {msg.position[i]}")
                    
                self.get_logger().info("Initial joint angles recorded.")
                print(f"Info: Inital positions are {self.initial_joint_angles}")
                print("Initial joint angles recorded.")

            else: 
                print(f"Debug: Inital positions are {self.initial_joint_angles}")
                for i in range(len(msg.name)):
                    joint_name = msg.name[i]
                    if joint_name in self.initial_joint_angles:
                        current_angle = msg.position[i]
                        initial_angle = self.initial_joint_angles[joint_name]
                        if abs(current_angle - initial_angle) > 0.001:  # Check if angle has changed significantly
                            self.get_logger().info(f"Current angle of {joint_name}: {current_angle} radians. Restoring to initial angle.")
                            print(f"Current angle of {joint_name}: {current_angle} radians. Restoring to initial angle.")
                            self.restore_joint_angle(joint_name, current_angle)
                        else: 
                            self.get_logger().error(f"Error: Diffence '{abs(current_angle - initial_angle)}' too small to correct.")
                    else: 
                        self.get_logger().error(f"Error: Joint '{joint_name}' not found in initial joint angles.")


def main(args=None):
    rclpy.init(args=args)

    x1 = 0.06
    y1 = 0.14
    z1 = 0.06 
    m1 = 1.0

    ixx = (1/12) * m1 * (y1*y1+z1*z1)
    iyy = (1/12) * m1 * (x1*x1+z1*z1)
    izz = (1/12) * m1 * (x1*x1+y1*y1)

    # Define inertia properties
    inertia_properties = {
        'link_1': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_2': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_3': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_4': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_5': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_6': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_7': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_8': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_9': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        'link_10': {'mass': 1.0, 'ixx': ixx, 'iyy': iyy, 'izz': izz},
        # Add inertia properties for other links here
    }

    snake_robot_controller = SnakeRobotController(inertia_properties)

    try:
        rclpy.spin(snake_robot_controller)
    except KeyboardInterrupt:
        pass

    snake_robot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
