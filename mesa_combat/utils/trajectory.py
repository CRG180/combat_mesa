import numpy as np
import matplotlib.pyplot as plt
import math
from typing import Tuple, List

# For Mypy
Cord3D = Tuple[float,float,float]
Cord3DTime = Tuple[float,float,float,int]

def generate_curved_trajectory(origin:Cord3D, destination:Cord3D, 
                               peak_z:float, speed:float,
                               time_resolution=1.0) -> List[Cord3DTime]:
    """
    Generate a curved trajectory passing through the origin, mid-point (with max z), and destination.

    Parameters:
    - origin (tuple): (x, y, z) coordinates of the starting point.
    - destination (tuple): (x, y, z) coordinates of the ending point.
    - peak_z (float): Peak Z value to be reached in the trajectory.
    - speed (float): Speed of the projectile in meters per second.
    - time_resolution (float): Time resolution or interval for calculating the trajectory.

    Returns:
    - list of tuples: List of (x, y, z, time) coordinates representing the curved trajectory.
    """

    # Extract coordinates
    x_origin, y_origin, z_origin = origin
    x_destination, y_destination, z_destination = destination

    # Calculate the mid-point
    # x_midpoint = (x_origin + x_destination) / 2
    # y_midpoint = (y_origin + y_destination) / 2
    z_midpoint = z_origin + peak_z

    # Calculate the total travel distance
    total_distance = np.sqrt((x_destination - x_origin)**2 + (y_destination - y_origin)**2 + (z_destination - z_origin)**2)

    # Calculate the time it takes to travel the total distance at the specified speed
    total_time = total_distance / speed

    # Calculate the time coordinates at the specified resolution
    time_coordinates = np.arange(0, total_time, time_resolution)

    # Calculate the corresponding coordinates for each time point
    x_coordinates = np.interp(time_coordinates, [0, total_time], [x_origin, x_destination])
    y_coordinates = np.interp(time_coordinates, [0, total_time], [y_origin, y_destination])

    # Fit a quadratic curve for the z-coordinates
    z_coefficients = np.polyfit([0, total_time / 2, total_time], [z_origin, z_midpoint, z_destination], 2)
    z_curve = np.poly1d(z_coefficients)

    # Calculate z-coordinates based on the quadratic curve
    z_coordinates = z_curve(time_coordinates)

    # Combine coordinates into a list of tuples with time information
    curved_trajectory = list(zip(x_coordinates, y_coordinates, z_coordinates, time_coordinates))

    # Ensure the last point lands on the target
    curved_trajectory.append((x_destination, y_destination, 
                              z_destination, math.floor(total_time + time_resolution)))

    return curved_trajectory

if __name__ == '__main__':
    # Example usage:
    origin_point = (200, 100, 1)
    destination_point = (1000, 1000, 0)
    peak_z_value = 5000
    speed_value = 100  # meters per second
    time_resolution_value = 1  # seconds

    curved_trajectory = generate_curved_trajectory(origin_point, destination_point,
                                                peak_z_value, speed_value, time_resolution_value)


    print(curved_trajectory)
    
    # Plotting the curved trajectory in 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract x, y, z, time coordinates from the curved trajectory
    x_curved, y_curved, z_curved, time_curved = zip(*curved_trajectory)

    # Plot the trajectory
    ax.plot(x_curved, y_curved, z_curved, label='Curved Trajectory', color='blue', marker='o')

    # Plot start and end points
    ax.scatter(*origin_point, color='red', label='Start Point')
    ax.scatter(*destination_point, color='green', label='End Point')

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Curved Trajectory')

    # Show legend
    ax.legend()

    # Add time labels
    for i, txt in enumerate(time_curved):
        ax.text(x_curved[i], y_curved[i], z_curved[i], f'{txt:.0f} s', fontsize=8)

    # Show the plot
    plt.show()