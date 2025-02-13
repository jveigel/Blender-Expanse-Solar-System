import numpy as np
from typing import Tuple, List

def calculate_orbit_point(a: float, e: float, i: float, Ω: float, ω: float, 
                         true_anomaly: float) -> np.ndarray:
    """
    Calculate position vector for a point in an orbit.
    
    Parameters:
    a: semi-major axis (AU or km)
    e: eccentricity
    i: inclination (radians)
    Ω: longitude of ascending node (radians)
    ω: argument of periapsis (radians)
    true_anomaly: true anomaly (radians)
    
    Returns:
    np.ndarray: 3D position vector
    """
    # Calculate radius
    r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
    
    # Position in orbital plane
    x = r * np.cos(true_anomaly)
    y = r * np.sin(true_anomaly)
    
    # Rotation matrices
    R_ω = np.array([[np.cos(ω), -np.sin(ω), 0],
                    [np.sin(ω), np.cos(ω), 0],
                    [0, 0, 1]])
    
    R_i = np.array([[1, 0, 0],
                    [0, np.cos(i), -np.sin(i)],
                    [0, np.sin(i), np.cos(i)]])
    
    R_Ω = np.array([[np.cos(Ω), -np.sin(Ω), 0],
                    [np.sin(Ω), np.cos(Ω), 0],
                    [0, 0, 1]])
    
    # Apply rotations
    pos = np.array([x, y, 0])
    pos = R_ω @ pos
    pos = R_i @ pos
    pos = R_Ω @ pos
    
    return pos

def median_orbit_distance(orbit1_params: Tuple, orbit2_params: Tuple, 
                         num_points: int = 1000) -> float:
    """
    Calculate the median distance between two orbits.
    
    Parameters:
    orbit1_params: Tuple of (a, e, i, Ω, ω) for first orbit
    orbit2_params: Tuple of (a, e, i, Ω, ω) for second orbit
    num_points: Number of points to sample along each orbit
    
    Returns:
    float: Median distance between the orbits
    """
    # Generate true anomaly values
    true_anomalies = np.linspace(0, 2*np.pi, num_points)
    
    # Calculate points along both orbits
    orbit1_points = np.array([calculate_orbit_point(*orbit1_params, v) 
                             for v in true_anomalies])
    orbit2_points = np.array([calculate_orbit_point(*orbit2_params, v) 
                             for v in true_anomalies])
    
    # Calculate distances between all pairs of points
    distances = []
    for p1 in orbit1_points:
        for p2 in orbit2_points:
            dist = np.linalg.norm(p2 - p1)
            distances.append(dist)
    
    # Return median distance
    return np.median(distances)

# Example usage:
if __name__ == "__main__":
    # Example: Earth-like and Mars-like orbits
    earth_orbit = (1.0, 0.0167, 0.0, 0.0, 0.0)  # Simplified Earth orbit
    mars_orbit = (1.524, 0.0934, 0.032, 0.865, 0.434)  # Simplified Mars orbit
    
    median_dist = median_orbit_distance(earth_orbit, mars_orbit)
    print(f"Median distance between orbits: {median_dist:.3f} AU")