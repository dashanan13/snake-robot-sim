import rclpy
from rclpy.node import Node
from gazebo_msgs.msg import ContactsState
from std_msgs.msg import Float64
import math

class SnakeRobotController(Node):
    def __init__(self):
        super().__init__('snake_robot_controller')
        self.contact_subscribers = []
        self.joint_torque_publishers = {}
        self.obstacle_forces = {}
        self.joint_number_to_control = 6  # Default joint number to control

        # Subscribe to contact sensors of each link
        for i in range(1, 11):  # Assuming links are numbered from 1 to 10
            contact_topic = f'/link{i}_bumper_states'
            subscriber = self.create_subscription(ContactsState, contact_topic, self.contact_callback, 10)
            self.contact_subscribers.append(subscriber)

        # Initialize torque publishers for each joint
        for i in range(2, 10):  # Assuming joints are numbered from 2 to 9
            torque_topic = f'/joints{i}_controllers/commands'
            self.joint_torque_publishers[f'joint_{i}'] = self.create_publisher(Float64, torque_topic, 10)

        # Create a timer to call the function repeatedly
        self.timer_period = 1.0  # 1 second
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        print("Timer callback triggered.")
        print("Processing links...")
        rclpy.spin_once(self)
        print("All links processed.")
        print("Dumping the variable obstacle_forces:")
        print(self.obstacle_forces)
        self.apply_torque_to_push_obstacle()

    def contact_callback(self, msg):
        # Clear previous obstacle forces
        self.obstacle_forces.clear()
        
        # Check if any contact occurred with an obstacle
        for contact in msg.states:
            collision1_name = contact.collision1_name.split('::')[1]
            collision2_name = contact.collision2_name.split('::')[1]
            
            if collision1_name.startswith('obstacle') or collision2_name.startswith('obstacle'):
                force = math.sqrt(contact.total_wrench.force.x**2 + contact.total_wrench.force.y**2 + contact.total_wrench.force.z**2)
                link_name = collision1_name if collision1_name.startswith('link') else collision2_name
                obstacle_name = collision2_name if collision2_name.startswith('obstacle') else collision1_name
                self.obstacle_forces[link_name] = (obstacle_name, force)

    def apply_torque_to_push_obstacle(self):
        print("Processing values now...")
        if not self.obstacle_forces:
            print("No contact with obstacles detected.")
            return
        
        # Calculate total force experienced by the robot due to contact with obstacles
        total_force = sum([force for (_, force) in self.obstacle_forces.values()])

        # Apply torque to the specified joint to push the obstacle behind
        torque_msg = Float64()
        # Assuming simple proportional control law: torque = K * total_force
        K = 1.0  # Proportional gain
        torque = K * total_force
        # Apply torque in the positive direction to move forward
        if self.joint_number_to_control % 2 == 0:
            torque_msg.data = torque
        else:
            torque_msg.data = -torque  # Invert torque for odd numbered joints
        self.joint_torque_publishers[f'joint_{self.joint_number_to_control}'].publish(torque_msg)

        # Print out information for each link that has contact with an obstacle
        if self.obstacle_forces:
            print("Contact with obstacles detected:")
            for link_name, (obstacle_name, force) in self.obstacle_forces.items():
                print(f"Link '{link_name}' has contact with obstacle '{obstacle_name}', force: {force}, applied torque: {torque}")
        else:
            print("No contact with obstacles detected.")

def main(args=None):
    rclpy.init(args=args)
    controller = SnakeRobotController()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
