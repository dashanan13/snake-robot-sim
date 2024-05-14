import math
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from std_msgs.msg import Float64MultiArray, String, Float64 
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray, String, Float64 
import numpy as np

# Constants
JOINT_COUNT = 9
TIMER_PERIOD = 1.0  # Update every 2 seconds
K_P = 0.1           # Proportional gain
K_I = 0.1          # Integral gain
K_D = 0.5          # Derivative gain

FeedBack = np.empty(9,dtype=float)  
Vel_FeedBack = np.empty(9,dtype=float)
set_point = np.empty(9,dtype=float)  
U_Value = np.empty(9,dtype=float)
Velocity = np.empty(9,dtype=float)
Acceleration = np.empty(9,dtype=float)

class SnakeRobotController(Node):
    def __init__(self):
        super().__init__('snake_robot_controller')
        self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)

        # Initialize publishers for each joint controller
        self.joint_publishers = []
        for i in range(1, JOINT_COUNT + 1):
            joint_effort_controller = self.create_publisher(Float64MultiArray, f'/joints{i}_controllers/commands', 10)
            self.joint_publishers.append(joint_effort_controller)

        # Initialize subscription to joint states
        self.joint_sub = self.create_subscription(Float64MultiArray, 'joint_states', self.joint_state_callback, 10)

        # Initialize timer for control loop
        self.timer = self.create_timer(TIMER_PERIOD, self.timer_callback)

        self.error_data = Float64()

        # Initialize PID parameters
        self.k_p = K_P
        self.k_i = K_I
        self.k_d = K_D
        self.error_integral = np.zeros(JOINT_COUNT)
        self.last_error = np.zeros(JOINT_COUNT)

        # Initialize feedback joint angles
        self.feedback_angles = np.zeros(JOINT_COUNT)

        # Initialize desired joint angles
        self.desired_angles = np.zeros(JOINT_COUNT)

        # Initialize time variable
        self.time = 0

    def joint_state_callback(self, msg):
        # Callback function to update feedback joint angles
        self.feedback_angles = np.array(msg.data)

    def phi_angle_generator_at_t(self, t):
        # Define parameters for sine wave generation
        amplitude = 65  # Amplitude set to pi radians (180 degrees)
        phase_shift = 0.78  # Adjusted phase shift for regular distribution

        # Generate sine wave angles for each joint
        angles = np.zeros(JOINT_COUNT)
        velocity = np.zeros(JOINT_COUNT)
        acceleration = np.zeros(JOINT_COUNT)
        return_array = np.array([])

        for i in range(JOINT_COUNT):
            # Define amplitude and frequency for each joint
            
            frequency = 0.5            # Frequency is constant for all joints

            # Generate sine wave angle for the joint, adjusting with time t and joint index
            angles[i] = amplitude * np.sin(frequency * t * i * phase_shift)
            velocity[i] = amplitude * np.sin(frequency * t * i * phase_shift)
            acceleration[i] = amplitude * np.sin(frequency * t * i * phase_shift)
            
            print(amplitude, frequency, t, angles[i], math.degrees(angles[i]))
            
        return_array = np.array([angles, velocity, acceleration])

        return return_array
    

    def pid_control(self,msg):
        # Calculate errors
        feedback_temp = np.empty(9,dtype=float)
        velocity_temp = np.empty(9,dtype=float)   
        for i in range(0,9):
            feedback_temp[i] = msg.position[i]  
            velocity_temp[i] = msg.velocity[i]
            
            FeedBack[i] = feedback_temp[i]
            Vel_FeedBack[i] = velocity_temp[i]


    def timer_callback(self):
        # Update time
        self.time += TIMER_PERIOD

        # Generate desired joint angles
        Angles, Velocity , Acceleration = self.phi_angle_generator_at_t(self.time)
        for i in range(0,9):
            U_Value[i] = 1*((Acceleration[i] + self.k_d * ( set_point[i] - FeedBack[i] ) + self.k_p * (Velocity[i] - Vel_FeedBack[i])))

            self.error_data.data = (Angles[i])#*(3.14/180) 
            self.create_publisher(Float64, 'position'+str(i), 10).publish(self.error_data)

            self.error_data.data =(FeedBack[i])*(180/3.14)
            self.create_publisher(Float64, 'position_feedback_'+str(i), 10).publish(self.error_data)

            self.error_data.data = Velocity[i] 
            self.create_publisher(Float64, 'velocity'+str(i), 10).publish(self.error_data)

            self.error_data.data = Vel_FeedBack[i]
            self.create_publisher(Float64, 'velocity_feedback_'+str(i), 10).publish(self.error_data)


        # Publish control effort to each joint controller
        for i, effort_publisher in enumerate(self.joint_publishers):
            msg = Float64MultiArray()
            msg.data = [U_Value[i]]
            effort_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = SnakeRobotController()
    rclpy.spin(controller)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
