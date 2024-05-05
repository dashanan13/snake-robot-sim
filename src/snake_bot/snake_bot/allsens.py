import rclpy
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped
import matplotlib.pyplot as plt
from collections import deque
from tf2_msgs.msg import TFMessage
import tf2_ros

class ForceTorqueVisualizer(Node):

    def __init__(self):
        super().__init__('force_torque_visualizer')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        #Subscriber for position from /tf

        self.tfsub = self.create_subscription(TFMessage, '/tf', self.tf_callback, 10)
        self.num_joints=2
        
        #Subscriber for force and torque of all joints

        self.subscription1 = self.create_subscription(WrenchStamped,'/joint_1',self.joint_1_callback,10)
        self.subscription2 = self.create_subscription(WrenchStamped,'/joint_2',self.joint_2_callback,10)
        self.subscription3 = self.create_subscription(WrenchStamped,'/joint_3',self.joint_3_callback,10)
        self.subscription4 = self.create_subscription(WrenchStamped,'/joint_4',self.joint_4_callback,10)
        self.subscription5 = self.create_subscription(WrenchStamped,'/joint_5',self.joint_5_callback,10)
        self.subscription6 = self.create_subscription(WrenchStamped,'/joint_6',self.joint_6_callback,10)
        self.subscription7 = self.create_subscription(WrenchStamped,'/joint_7',self.joint_7_callback,10)
        self.subscription8 = self.create_subscription(WrenchStamped,'/joint_8',self.joint_8_callback,10)
        self.subscription9 = self.create_subscription(WrenchStamped,'/joint_9',self.joint_9_callback,10)

        self.paused = False
        self.declare()
        self.fig, self.axs = plt.subplots(3, 4, figsize=(15, 12))
        self.fig.canvas.mpl_connect('key_press_event', self.toggle_pause)
    
    def declare(self):          #Method to declare the requirements
        len=10

        self.position_x = deque(maxlen=len)         #limit max size
        self.position_y = deque(maxlen=len)
        self.position_z = deque(maxlen=len)

        self.force_x_data = [deque(maxlen=len) for _ in range(9)]
        self.force_y_data = [deque(maxlen=len) for _ in range(9)]
        self.force_z_data = [deque(maxlen=len) for _ in range(9)]
        self.torque_x_data = [deque(maxlen=len) for _ in range(9)]
        self.torque_y_data = [deque(maxlen=len) for _ in range(9)]
        self.torque_z_data = [deque(maxlen=len) for _ in range(9)]
    
    def plot(self):             #Method to plot all the data
        for i in range(9):
            row = i // 3
            col = i % 3
            print(row, col)

            self.axs[row, col].clear()
            self.axs[row, col].plot(self.force_x_data[i], label=f'Joint {i+1} Force X')
            self.axs[row, col].plot(self.torque_x_data[i], label=f'Joint {i+1} Torque X')
            self.axs[row, col].legend(loc='upper left', bbox_to_anchor=(1, 1))
            self.axs[row, col].set_title(f'Joint {i+1} Values')
            self.axs[row, col].set_xlabel('Time')
            self.axs[row, col].set_ylabel('Value')

        self.axs[0, 3].clear()     
        self.axs[0, 3].plot(self.position_x, label='X')   
        self.axs[0, 3].legend(loc='upper left', bbox_to_anchor=(1, 1))
        self.axs[0, 3].set_title('Position X Values')
        self.axs[0, 3].set_xlabel('Time')
        self.axs[0, 3].set_ylabel('Position X')

        self.axs[1, 3].clear()     
        self.axs[1, 3].plot(self.position_y, label='Y')   
        self.axs[1, 3].legend(loc='upper left', bbox_to_anchor=(1, 1))
        self.axs[1, 3].set_title('Position Y Values')
        self.axs[1, 3].set_xlabel('Time')
        self.axs[1, 3].set_ylabel('Position Y')

        self.axs[2, 3].clear()     
        self.axs[2, 3].plot(self.position_z, label='Z')   
        self.axs[2, 3].legend(loc='upper left', bbox_to_anchor=(1, 1))
        self.axs[2, 3].set_title('Position Z Values')
        self.axs[2, 3].set_xlabel('Time')
        self.axs[2, 3].set_ylabel('Position Z')

        plt.tight_layout()
        plt.pause(0.01)

    def toggle_pause(self, event):  #Method to pause the update of graph whenever needed
        if event.key == ' ':
            self.paused = not self.paused

    def tf_callback(self, msg):     #Callback for position
        if not self.paused:
            for transform in msg.transforms:
                if transform.child_frame_id == 'base_link':  # Replace 'model_name' with the name of your model
                    position = transform.transform.translation
                    pos_x = position.x
                    pos_y = position.y
                    pos_z = position.z
                    self.position_x.append(pos_x)
                    self.position_y.append(pos_y)
                    self.position_z.append(pos_z)

    def joint_1_callback(self, msg):            #Callbacks for joints states 
        if not self.paused:
            self._process_joint_data(msg, 0)

    def joint_2_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 1)

    def joint_3_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 2)

    def joint_4_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 3)

    def joint_5_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 4)

    def joint_6_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 5)

    def joint_7_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 6)

    def joint_8_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 7)

    def joint_9_callback(self, msg):
        if not self.paused:
            self._process_joint_data(msg, 8)

    def _process_joint_data(self, msg, index):      #assigning joint values to plot variables
        force_x = msg.wrench.force.x
        force_y = msg.wrench.force.y
        force_z = msg.wrench.force.z
        torque_x = msg.wrench.torque.x
        torque_y = msg.wrench.torque.y
        torque_z = msg.wrench.torque.z

        self.force_x_data[index].append(force_x)
        self.force_y_data[index].append(force_y)
        self.force_z_data[index].append(force_z)
        self.torque_x_data[index].append(torque_x)
        self.torque_y_data[index].append(torque_y)
        self.torque_z_data[index].append(torque_z)

        self.plot()

def main(args=None):    
    rclpy.init(args=args)

    force_torque_visualizer = ForceTorqueVisualizer()
    rclpy.spin(force_torque_visualizer)

    force_torque_visualizer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
