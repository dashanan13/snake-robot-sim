import rclpy
from rclpy.node import Node
from gazebo_msgs.msg import ContactsState
import matplotlib.pyplot as plt
from collections import deque


class ContactSubscriber(Node):

    def __init__(self):
        super().__init__('contact_subscriber')
        self.subscription0 = self.create_subscription(ContactsState,'/link10_bumper_states',self.contact10_callback,10)
        self.subscription1 = self.create_subscription(ContactsState,'/link2_bumper_states',self.contact2_callback,10)
        self.subscription2 = self.create_subscription(ContactsState,'/link3_bumper_states',self.contact3_callback,10)
        self.subscription3 = self.create_subscription(ContactsState,'/link4_bumper_states',self.contact4_callback,10)
        self.subscription4 = self.create_subscription(ContactsState,'/link5_bumper_states',self.contact5_callback,10)
        self.subscription5 = self.create_subscription(ContactsState,'/link6_bumper_states',self.contact6_callback,10)
        self.subscription6 = self.create_subscription(ContactsState,'/link7_bumper_states',self.contact7_callback,10)
        self.subscription7 = self.create_subscription(ContactsState,'/link8_bumper_states',self.contact8_callback,10)
        self.subscription8 = self.create_subscription(ContactsState,'/link9_bumper_states',self.contact9_callback,10)

        
        self.paused = False
        self.declare()
        self.fig, self.axs = plt.subplots(3, 3, figsize=(15, 12))
    
    def declare(self):          #Method to declare the requirements
        len=100


        self.contact_data = [deque(maxlen=len) for _ in range(9)]
        self.contact_data2 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data3 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data4 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data5 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data6 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data7 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data8 = [deque(maxlen=len) for _ in range(9)]
        self.contact_data9 = [deque(maxlen=len) for _ in range(9)]
    
    def contact2_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[1].append(1 if has_contact else 0)
    
    def contact3_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[2].append(1 if has_contact else 0)
    
    def contact4_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[3].append(1 if has_contact else 0)
    
    def contact5_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[4].append(1 if has_contact else 0)
    
    def contact6_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[5].append(1 if has_contact else 0)
    
    def contact7_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[6].append(1 if has_contact else 0)

    def contact8_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[7].append(1 if has_contact else 0)

    def contact9_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[8].append(1 if has_contact else 0)

    def contact10_callback(self, msg):
        has_contact = False
        for collision in msg.states:
            # Check if the collision involves an obstacle (not ground)
            if "ground" not in collision.collision1_name and "ground" not in collision.collision2_name:
                has_contact = True
                break
        self.contact_data[0].append(1 if has_contact else 0)
        self.plot_graph()

    def plot_graph(self):


        for i in range(9):
            row = i // 3
            col = i % 3
            print(row, col)

            self.axs[row, col].clear()
            self.axs[row, col].plot(self.contact_data[i], label=f'link {i+1} ')
            self.axs[row, col].legend(loc='upper left', bbox_to_anchor=(1, 1))
            self.axs[row, col].set_title(f'link {i+1} Values')
            self.axs[row, col].set_xlabel('Time')
            self.axs[row, col].set_ylabel('Value')

        plt.tight_layout()
        plt.pause(0.01)


def main(args=None):
    rclpy.init(args=args)
    contact_subscriber = ContactSubscriber()
    rclpy.spin(contact_subscriber)
    contact_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
