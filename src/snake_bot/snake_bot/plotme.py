import matplotlib.pyplot as plt
import numpy as np

# Function to generate sine wave values for one joint angle
def phi_angle_generator_at_t(timer, var_a, var_w, var_d, var_phi0, var_phi1):
    N = 10
    a = var_a                            # Alpha value of the equation
    w = var_w                           # Freq_w of the equation of the angle
    d = var_d                           # Delta, which is the value of the phase shift in the equation of the angle 0.698132 
    phi0 = var_phi0                    # Offset angle in positive dir
    phi1 = var_phi1                    # Offset angle in negative dir
    temp_JA = np.empty(N-1, dtype=float)
    for i in range(0, N - 1):
        temp_JA[i] = (a * np.sin(w * timer + i * d) + phi0 - phi1)
    return temp_JA

# Parameters
var_a = 65
var_w = 0.45
var_d = 0.78
var_phi0 = 0
var_phi1 = 0

# Time values
time_values = np.linspace(0, 10, 1000)  # Generate time values from 0 to 10 seconds

# Generate sine wave values for one joint angle over time
joint_angle_values = phi_angle_generator_at_t(time_values, var_a, var_w, var_d, var_phi0, var_phi1)

# Plot the sine wave
plt.plot(time_values, joint_angle_values)
plt.xlabel('Time (s)')
plt.ylabel('Joint Angle (degrees)')
plt.title('Sin Wave Pattern for One Joint Angle')
plt.grid(True)
plt.show()
