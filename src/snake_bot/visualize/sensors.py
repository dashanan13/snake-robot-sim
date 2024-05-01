import rclpy
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped
import matplotlib.pyplot as plt
from collections import deque

class ForceTorqueVisualizer(Node):

    def __init__(self):
        super().__init__('force_torque_visualizer')
        self.num_joints=2
        
        self.subscription1 = self.create_subscription(WrenchStamped,'/joint_1',self.joint_1_callback,10)
        self.subscription2 = self.create_subscription(WrenchStamped,'/joint_2',self.joint_2_callback,10)
        self.subscription3 = self.create_subscription(WrenchStamped,'/joint_3',self.joint_3_callback,10)
        self.subscription4 = self.create_subscription(WrenchStamped,'/joint_4',self.joint_4_callback,10)
        self.subscription5 = self.create_subscription(WrenchStamped,'/joint_5',self.joint_5_callback,10)
        self.subscription6 = self.create_subscription(WrenchStamped,'/joint_6',self.joint_6_callback,10)
        self.subscription7 = self.create_subscription(WrenchStamped,'/joint_7',self.joint_7_callback,10)
        self.subscription8 = self.create_subscription(WrenchStamped,'/joint_8',self.joint_8_callback,10)
        self.subscription9 = self.create_subscription(WrenchStamped,'/joint_9',self.joint_9_callback,10)
        self.subscription1  # prevent unused variable warning
        self.subscription2
        self.subscription3
        self.subscription4
        self.subscription5
        self.subscription6
        self.subscription7
        self.subscription8
        self.subscription9

        self.declare()
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8))
    
    def declare(self):
        self.joint1_force_x_data = deque(maxlen=100)  # Limiting the deque size to 100 for better visualization
        self.joint1_force_y_data = deque(maxlen=100)
        self.joint1_force_z_data = deque(maxlen=100)
        self.joint1_torque_x_data = deque(maxlen=100)
        self.joint1_torque_y_data = deque(maxlen=100)
        self.joint1_torque_z_data = deque(maxlen=100)

        self.joint2_force_x_data = deque(maxlen=100)  
        self.joint2_force_y_data = deque(maxlen=100)
        self.joint2_force_z_data = deque(maxlen=100)
        self.joint2_torque_x_data = deque(maxlen=100)
        self.joint2_torque_y_data = deque(maxlen=100)
        self.joint2_torque_z_data = deque(maxlen=100)

        self.joint3_force_x_data = deque(maxlen=100)  
        self.joint3_force_y_data = deque(maxlen=100)
        self.joint3_force_z_data = deque(maxlen=100)
        self.joint3_torque_x_data = deque(maxlen=100)
        self.joint3_torque_y_data = deque(maxlen=100)
        self.joint3_torque_z_data = deque(maxlen=100)

        self.joint4_force_x_data = deque(maxlen=100)  
        self.joint4_force_y_data = deque(maxlen=100)
        self.joint4_force_z_data = deque(maxlen=100)
        self.joint4_torque_x_data = deque(maxlen=100)
        self.joint4_torque_y_data = deque(maxlen=100)
        self.joint4_torque_z_data = deque(maxlen=100)

        self.joint5_force_x_data = deque(maxlen=100)  
        self.joint5_force_y_data = deque(maxlen=100)
        self.joint5_force_z_data = deque(maxlen=100)
        self.joint5_torque_x_data = deque(maxlen=100)
        self.joint5_torque_y_data = deque(maxlen=100)
        self.joint5_torque_z_data = deque(maxlen=100)

        self.joint6_force_x_data = deque(maxlen=100)  
        self.joint6_force_y_data = deque(maxlen=100)
        self.joint6_force_z_data = deque(maxlen=100)
        self.joint6_torque_x_data = deque(maxlen=100)
        self.joint6_torque_y_data = deque(maxlen=100)
        self.joint6_torque_z_data = deque(maxlen=100)

        self.joint7_force_x_data = deque(maxlen=100)  
        self.joint7_force_y_data = deque(maxlen=100)
        self.joint7_force_z_data = deque(maxlen=100)
        self.joint7_torque_x_data = deque(maxlen=100)
        self.joint7_torque_y_data = deque(maxlen=100)
        self.joint7_torque_z_data = deque(maxlen=100)

        self.joint8_force_x_data = deque(maxlen=100)  
        self.joint8_force_y_data = deque(maxlen=100)
        self.joint8_force_z_data = deque(maxlen=100)
        self.joint8_torque_x_data = deque(maxlen=100)
        self.joint8_torque_y_data = deque(maxlen=100)
        self.joint8_torque_z_data = deque(maxlen=100)

        self.joint9_force_x_data = deque(maxlen=100)  
        self.joint9_force_y_data = deque(maxlen=1009)
        self.joint9_force_z_data = deque(maxlen=100)
        self.joint9_torque_x_data = deque(maxlen=100)
        self.joint9_torque_y_data = deque(maxlen=100)
        self.joint9_torque_z_data = deque(maxlen=100)
    
    def plot(self):
        self.axs[0].clear()
        self.axs[0].plot(self.joint1_force_x_data, label='Joint 1 Force X')
        self.axs[0].plot(self.joint2_force_x_data, label='Joint 2 Force X')
        self.axs[0].plot(self.joint3_force_x_data, label='Joint 3 Force X')
        self.axs[0].plot(self.joint4_force_x_data, label='Joint 4 Force X')
        self.axs[0].plot(self.joint5_force_x_data, label='Joint 5 Force X')
        self.axs[0].plot(self.joint6_force_x_data, label='Joint 6 Force X')
        self.axs[0].plot(self.joint7_force_x_data, label='Joint 7 Force X')
        self.axs[0].plot(self.joint8_force_x_data, label='Joint 8 Force X')
        self.axs[0].plot(self.joint9_force_x_data, label='Joint 9 Force X')
        self.axs[0].legend()
        self.axs[0].set_title('Force X Values')
        self.axs[0].set_xlabel('Time')
        self.axs[0].set_ylabel('Force X (N)')

        self.axs[1].clear()
        self.axs[1].plot(self.joint1_torque_x_data, label='Joint 1 Torque X')
        self.axs[1].plot(self.joint2_torque_x_data, label='Joint 2 Torque X')
        self.axs[1].plot(self.joint3_torque_x_data, label='Joint 3 Torque X')
        self.axs[1].plot(self.joint4_torque_x_data, label='Joint 4 Torque X')
        self.axs[1].plot(self.joint5_torque_x_data, label='Joint 5 Torque X')
        self.axs[1].plot(self.joint6_torque_x_data, label='Joint 6 Torque X')
        self.axs[1].plot(self.joint7_torque_x_data, label='Joint 7 Torque X')
        self.axs[1].plot(self.joint8_torque_x_data, label='Joint 8 Torque X')
        self.axs[1].plot(self.joint9_torque_x_data, label='Joint 9 Torque X')
        self.axs[1].legend()
        self.axs[1].set_title('Torque X Values')
        self.axs[1].set_xlabel('Time')
        self.axs[1].set_ylabel('Torque X (Nm)')

        plt.tight_layout()
        plt.pause(0.01)


        

    def joint_1_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint1_force_x_data.append(force_x)
        self.joint1_force_y_data.append(force_y)
        self.joint1_force_z_data.append(force_z)
        self.joint1_torque_x_data.append(torque_x)
        self.joint1_torque_y_data.append(torque_y)
        self.joint1_torque_z_data.append(torque_z)
    
    def joint_2_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint2_force_x_data.append(force_x)
        self.joint2_force_y_data.append(force_y)
        self.joint2_force_z_data.append(force_z)
        self.joint2_torque_x_data.append(torque_x)
        self.joint2_torque_y_data.append(torque_y)
        self.joint2_torque_z_data.append(torque_z)
    
    def joint_3_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint3_force_x_data.append(force_x)
        self.joint3_force_y_data.append(force_y)
        self.joint3_force_z_data.append(force_z)
        self.joint3_torque_x_data.append(torque_x)
        self.joint3_torque_y_data.append(torque_y)
        self.joint3_torque_z_data.append(torque_z)
    
    def joint_4_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint4_force_x_data.append(force_x)
        self.joint4_force_y_data.append(force_y)
        self.joint4_force_z_data.append(force_z)
        self.joint4_torque_x_data.append(torque_x)
        self.joint4_torque_y_data.append(torque_y)
        self.joint4_torque_z_data.append(torque_z)

    def joint_5_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint5_force_x_data.append(force_x)
        self.joint5_force_y_data.append(force_y)
        self.joint5_force_z_data.append(force_z)
        self.joint5_torque_x_data.append(torque_x)
        self.joint5_torque_y_data.append(torque_y)
        self.joint5_torque_z_data.append(torque_z)
    
    def joint_6_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint6_force_x_data.append(force_x)
        self.joint6_force_y_data.append(force_y)
        self.joint6_force_z_data.append(force_z)
        self.joint6_torque_x_data.append(torque_x)
        self.joint6_torque_y_data.append(torque_y)
        self.joint6_torque_z_data.append(torque_z)

    def joint_7_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint7_force_x_data.append(force_x)
        self.joint7_force_y_data.append(force_y)
        self.joint7_force_z_data.append(force_z)
        self.joint7_torque_x_data.append(torque_x)
        self.joint7_torque_y_data.append(torque_y)
        self.joint7_torque_z_data.append(torque_z)
    
    def joint_8_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint8_force_x_data.append(force_x)
        self.joint8_force_y_data.append(force_y)
        self.joint8_force_z_data.append(force_z)
        self.joint8_torque_x_data.append(torque_x)
        self.joint8_torque_y_data.append(torque_y)
        self.joint8_torque_z_data.append(torque_z)
    
    def joint_9_callback(self, msg):
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.joint9_force_x_data.append(force_x)
        self.joint9_force_y_data.append(force_y)
        self.joint9_force_z_data.append(force_z)
        self.joint9_torque_x_data.append(torque_x)
        self.joint9_torque_y_data.append(torque_y)
        self.joint9_torque_z_data.append(torque_z)

        self.plot()
    


        



def main(args=None):
    rclpy.init(args=args)

    force_torque_visualizer = ForceTorqueVisualizer()
    rclpy.spin(force_torque_visualizer)

    force_torque_visualizer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
