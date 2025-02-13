import numpy as np
import matplotlib.pyplot as plt

class PatchedConicTrajectory:
    def __init__(self):
        # Gravitational constants (m^3 kg^-1 s^-2)
        self.G = 6.67430e-11
        
        # Celestial body properties (approximate values)
        self.sun_mass = 1.989e30
        self.earth_mass = 5.97e24
        self.mars_mass = 6.39e23
        
        # Orbital radii (meters)
        self.earth_orbit_radius = 1.496e11  # 1 AU
        self.mars_orbit_radius = 2.279e11   # 1.52 AU
        
        # Average orbital velocities (m/s)
        self.earth_velocity = 29.78e3
        self.mars_velocity = 24.07e3

    def calculate_hohmann_transfer(self):
        """
        Calculate a simple Hohmann transfer orbit between Earth and Mars
        """
        # Semi-major axis of transfer orbit
        a_transfer = (self.earth_orbit_radius + self.mars_orbit_radius) / 2
        
        # Transfer orbit velocity calculations
        # Velocity at perihelion (leaving Earth's orbit)
        v1 = np.sqrt(self.G * self.sun_mass * (2/self.earth_orbit_radius - 1/a_transfer))
        
        # Velocity at aphelion (entering Mars' orbit)
        v2 = np.sqrt(self.G * self.sun_mass * (2/self.mars_orbit_radius - 1/a_transfer))
        
        # Transfer time (half of the elliptical orbit period)
        transfer_time = np.pi * np.sqrt(a_transfer**3 / (self.G * self.sun_mass))
        
        return {
            'transfer_orbit_semi_major_axis': a_transfer,
            'departure_velocity': v1,
            'arrival_velocity': v2,
            'transfer_time': transfer_time / (24 * 3600)  # Convert to days
        }

    def visualize_trajectory(self):
        """
        Create a simple visualization of the transfer orbit
        """
        trajectory = self.calculate_hohmann_transfer()
        
        # Plotting
        plt.figure(figsize=(10, 6))
        
        # Sun
        plt.scatter(0, 0, color='yellow', s=200, label='Sun')
        
        # Earth orbit
        earth_circle = plt.Circle((0, 0), self.earth_orbit_radius, 
                                  fill=False, color='blue', linestyle='--', label='Earth Orbit')
        plt.gca().add_artist(earth_circle)
        
        # Mars orbit
        mars_circle = plt.Circle((0, 0), self.mars_orbit_radius, 
                                 fill=False, color='red', linestyle='--', label='Mars Orbit')
        plt.gca().add_artist(mars_circle)
        
        plt.title('Simplified Patched Conic Transfer Orbit')
        plt.xlabel('Distance (m)')
        plt.ylabel('Distance (m)')
        plt.axis('equal')
        plt.legend()
        plt.grid(True, linestyle=':')
        plt.tight_layout()
        plt.show()

    def mission_summary(self):
        """
        Print a summary of the mission parameters
        """
        trajectory = self.calculate_hohmann_transfer()
        print("Patched Conic Trajectory to Mars:")
        print(f"Transfer Orbit Semi-Major Axis: {trajectory['transfer_orbit_semi_major_axis']:,.0f} m")
        print(f"Departure Velocity: {trajectory['departure_velocity']:,.2f} m/s")
        print(f"Arrival Velocity: {trajectory['arrival_velocity']:,.2f} m/s")
        print(f"Transfer Time: {trajectory['transfer_time']:,.2f} days")

def main():
    # Create and run the patched conic trajectory simulation
    mars_mission = PatchedConicTrajectory()
    
    # Calculate and print mission parameters
    mars_mission.mission_summary()
    
    # Visualize the trajectory
    mars_mission.visualize_trajectory()

if __name__ == "__main__":
    main()