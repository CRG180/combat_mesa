import unittest
from mesa_combat.utils.trajectory import generate_curved_trajectory
import math
class TestGenerateCurvedTrajectory(unittest.TestCase):

    def test_generate_curved_trajectory(self):
        # Define test parameters
        origin_point = (200, 100, 1)
        destination_point = (1000, 1000, 0)
        peak_z_value = 5000
        speed_value = 100  # meters per second
        time_resolution_value = 1  # seconds

        # Call the function
        curved_trajectory = generate_curved_trajectory(origin_point, destination_point,
                                                      peak_z_value, speed_value, time_resolution_value)

        # Assertions
        self.assertIsInstance(curved_trajectory, list)
        self.assertTrue(all(isinstance(coord, tuple) and len(coord) == 4 for coord in curved_trajectory))
        self.assertEqual(curved_trajectory[0], (*origin_point, 0))
        self.assertEqual(curved_trajectory[-1], (*destination_point, math.floor(len(curved_trajectory) * time_resolution_value)))

if __name__ == '__main__':
    unittest.main()