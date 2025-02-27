import bpy  # type: ignore
import math
import numpy as np
from mathutils import Vector  # type: ignore
from typing import Dict, List, Tuple, Any, Optional
import time

# Start timing
start_time = time.time()

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Planet data: J2000 epoch values (NASA DE440/DE441)
planets = {
    'Mercury': {'a': 0.387098, 'e': 0.205630, 'inc': 7.005, 'node': 48.331, 'peri': 29.124},
    'Venus': {'a': 0.723332, 'e': 0.006772, 'inc': 3.394, 'node': 76.680, 'peri': 54.884},
    'Earth': {'a': 1.000000, 'e': 0.016708, 'inc': 0.000, 'node': 0.000, 'peri': 102.937},
    'Mars': {'a': 1.523679, 'e': 0.093401, 'inc': 1.850, 'node': 49.558, 'peri': 286.502},
    'Ceres': {'a': 2.765348, 'e': 0.075823, 'inc': 10.593, 'node': 80.393, 'peri': 73.597},
    'Eros': {'a': 1.458432, 'e': 0.222974, 'inc': 10.829, 'node': 304.435, 'peri': 178.641},
    'Jupiter': {'a': 5.202561, 'e': 0.048498, 'inc': 1.303, 'node': 100.556, 'peri': 275.066},
    'Saturn': {'a': 9.537070, 'e': 0.054309, 'inc': 2.485, 'node': 113.715, 'peri': 338.716},
    'Uranus': {'a': 19.191264, 'e': 0.047318, 'inc': 0.773, 'node': 74.006, 'peri': 96.998},
    'Neptune': {'a': 30.068963, 'e': 0.008676, 'inc': 1.770, 'node': 131.783, 'peri': 273.187},
    'Pluto': {'a': 39.482117, 'e': 0.248897, 'inc': 17.140, 'node': 110.299, 'peri': 113.834}
}

# List of planet pairs to analyze
planet_pairs = [
    ('Earth', 'Mars'),
    ('Earth', 'Ceres'),
    ('Mars', 'Ceres'),
    ('Earth', 'Jupiter'),
    ('Mars', 'Jupiter'),
    ('Jupiter', 'Saturn'),
    ('Saturn', 'Ceres'),
    ('Neptune', 'Uranus')
]

# Configuration
NUM_POINTS = 500  # Balance between accuracy and speed
CURVE_RESOLUTION = 100  # Number of points for orbit visualization

# Cache for orbital points to avoid recalculation
orbital_points_cache: Dict[str, List[Vector]] = {}

def precompute_trig_values(data: Dict[str, float]) -> Dict[str, float]:
    """Precompute trigonometric values for orbital calculations."""
    inc_rad = math.radians(data['inc'])
    node_rad = math.radians(data['node'])
    peri_rad = math.radians(data['peri'])
    
    return {
        'a': data['a'],
        'e': data['e'],
        'cos_inc': math.cos(inc_rad),
        'sin_inc': math.sin(inc_rad),
        'cos_node': math.cos(node_rad),
        'sin_node': math.sin(node_rad),
        'cos_peri': math.cos(peri_rad),
        'sin_peri': math.sin(peri_rad)
    }

# Precompute trigonometric values for all planets
precomputed_planet_data = {name: precompute_trig_values(data) for name, data in planets.items()}

def calculate_point_on_orbit(data: Dict[str, float], true_anomaly: float) -> Vector:
    """Calculate 3D position at a given true anomaly using precomputed values."""
    # Get orbital parameters
    a = data['a']
    e = data['e']
    
    # Calculate radius using polar form of ellipse
    r = a * (1 - e**2) / (1 + e * math.cos(true_anomaly))
    
    # Initial position in orbital plane
    x = r * math.cos(true_anomaly)
    y = r * math.sin(true_anomaly)
    
    # Apply rotations using precomputed values
    # 1. Rotate by perihelion
    x_peri = x * data['cos_peri'] - y * data['sin_peri']
    y_peri = x * data['sin_peri'] + y * data['cos_peri']
    
    # 2. Rotate by inclination
    y_inc = y_peri * data['cos_inc']
    z_inc = y_peri * data['sin_inc']
    
    # 3. Rotate by node
    x_final = x_peri * data['cos_node'] - y_inc * data['sin_node']
    y_final = x_peri * data['sin_node'] + y_inc * data['cos_node']
    
    return Vector((x_final, y_final, z_inc))

def get_orbital_points(planet_name: str, num_points: int = NUM_POINTS) -> List[Vector]:
    """Get or calculate orbital points with caching."""
    cache_key = f"{planet_name}_{num_points}"
    
    if cache_key in orbital_points_cache:
        return orbital_points_cache[cache_key]
    
    theta_values = np.linspace(0, 2*np.pi, num_points)
    points = [calculate_point_on_orbit(precomputed_planet_data[planet_name], t) for t in theta_values]
    
    # Cache the result
    orbital_points_cache[cache_key] = points
    return points

# Create collections for organization
def setup_collections() -> Tuple[Any, Any]:
    """Set up the collections structure."""
    scene_collection = bpy.context.scene.collection
    
    # Create Orbits collection if it doesn't exist
    if "Orbits" not in bpy.data.collections:
        orbits_collection = bpy.data.collections.new("Orbits")
        scene_collection.children.link(orbits_collection)
    else:
        orbits_collection = bpy.data.collections["Orbits"]
        
    # Create Distances collection if it doesn't exist
    if "Min_Max.Distances" not in bpy.data.collections:
        distances_collection = bpy.data.collections.new("Min_Max.Distances")
        scene_collection.children.link(distances_collection)
    else:
        distances_collection = bpy.data.collections["Min_Max.Distances"]
    
    return orbits_collection, distances_collection

# Set up the collections
orbits_collection, distances_collection = setup_collections()

def create_orbital_curve(planet_name: str, data: Dict[str, float], index: int, parent_object: Any) -> Any:
    """Create a Blender curve object for the orbit."""
    # Create the curve
    curve_data = bpy.data.curves.new(name=f"{index}.{planet_name}.Orbit", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 64
    curve_object = bpy.data.objects.new(f"{index}.{planet_name}.Orbit", curve_data)
    
    # Add to the orbits collection
    orbits_collection.objects.link(curve_object)
    
    # Set parent
    curve_object.parent = parent_object
    
    # Create the orbital path
    spline = curve_data.splines.new('NURBS')
    
    # Get points (use cached if available)
    if planet_name in planets:
        points = get_orbital_points(planet_name, CURVE_RESOLUTION)
    else:
        # For reference orbit or other special cases
        theta = np.linspace(0, 2*np.pi, CURVE_RESOLUTION)
        points = [calculate_point_on_orbit(precompute_trig_values(data), t) for t in theta]
    
    # Set the points in the spline
    spline.points.add(len(points)-1)
    for i, point in enumerate(points):
        spline.points[i].co = (point[0], point[1], point[2], 1)
    
    # Close the curve
    spline.use_cyclic_u = True
    
    return curve_object

def calculate_distance_matrix(points1: List[Vector], points2: List[Vector]) -> np.ndarray:
    """Calculate distance matrix between two sets of points using vectorized operations."""
    # Convert to numpy arrays for faster calculation
    np_points1 = np.array([[p.x, p.y, p.z] for p in points1])
    np_points2 = np.array([[p.x, p.y, p.z] for p in points2])
    
    # Calculate distances using broadcasting
    # This creates a matrix of shape (len(points1), len(points2))
    distances = np.zeros((len(points1), len(points2)))
    
    # Vectorized distance calculation
    for i in range(len(points1)):
        # Broadcasting subtraction
        diff = np_points1[i] - np_points2
        # Calculate Euclidean distance for all points at once
        distances[i] = np.sqrt(np.sum(diff**2, axis=1))
    
    return distances

def find_min_max_distance_points(planet1: str, planet2: str) -> Dict[str, Any]:
    """Find the points of minimum and maximum distance between two orbits."""
    # Get orbital points (cached)
    orbit1_points = get_orbital_points(planet1)
    orbit2_points = get_orbital_points(planet2)
    
    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(orbit1_points, orbit2_points)
    
    # Find minimum and maximum distances
    min_idx = np.unravel_index(np.argmin(distance_matrix), distance_matrix.shape)
    max_idx = np.unravel_index(np.argmax(distance_matrix), distance_matrix.shape)
    
    # Get corresponding theta values
    theta_values = np.linspace(0, 2*np.pi, NUM_POINTS)
    min_theta1 = theta_values[min_idx[0]]
    min_theta2 = theta_values[min_idx[1]]
    max_theta1 = theta_values[max_idx[0]]
    max_theta2 = theta_values[max_idx[1]]
    
    # Refine the search around the approximate minimum and maximum
    min_theta1, min_theta2 = refine_extremum(planet1, planet2, min_theta1, min_theta2, is_minimum=True)
    max_theta1, max_theta2 = refine_extremum(planet1, planet2, max_theta1, max_theta2, is_minimum=False)
    
    # Calculate final points and distances
    min_point1 = calculate_point_on_orbit(precomputed_planet_data[planet1], min_theta1)
    min_point2 = calculate_point_on_orbit(precomputed_planet_data[planet2], min_theta2)
    max_point1 = calculate_point_on_orbit(precomputed_planet_data[planet1], max_theta1)
    max_point2 = calculate_point_on_orbit(precomputed_planet_data[planet2], max_theta2)
    
    min_distance = (min_point1 - min_point2).length
    max_distance = (max_point1 - max_point2).length
    
    return {
        'min_distance': min_distance,
        'min_point1': min_point1,
        'min_point2': min_point2,
        'min_theta1': min_theta1,
        'min_theta2': min_theta2,
        'max_distance': max_distance,
        'max_point1': max_point1,
        'max_point2': max_point2,
        'max_theta1': max_theta1,
        'max_theta2': max_theta2
    }

def refine_extremum(planet1: str, planet2: str, theta1: float, theta2: float, 
                   is_minimum: bool = True, steps: int = 5, step_size: float = 0.001) -> Tuple[float, float]:
    """Refine the extremum point using gradient descent with adaptive step size."""
    current_theta1 = theta1
    current_theta2 = theta2
    planet1_data = precomputed_planet_data[planet1]
    planet2_data = precomputed_planet_data[planet2]
    
    for _ in range(steps):
        # Calculate current distance
        p1 = calculate_point_on_orbit(planet1_data, current_theta1)
        p2 = calculate_point_on_orbit(planet2_data, current_theta2)
        current_distance = (p1 - p2).length
        
        # Try small steps in each direction
        best_distance = current_distance if is_minimum else -current_distance
        best_thetas = (current_theta1, current_theta2)
        
        # Check gradient in 8 directions
        for dt1 in [-step_size, 0, step_size]:
            for dt2 in [-step_size, 0, step_size]:
                if dt1 == 0 and dt2 == 0:
                    continue
                
                new_theta1 = (current_theta1 + dt1) % (2*math.pi)
                new_theta2 = (current_theta2 + dt2) % (2*math.pi)
                
                p1_new = calculate_point_on_orbit(planet1_data, new_theta1)
                p2_new = calculate_point_on_orbit(planet2_data, new_theta2)
                new_distance = (p1_new - p2_new).length
                
                # Update if better (smaller for minimum, larger for maximum)
                if (is_minimum and new_distance < best_distance) or \
                   (not is_minimum and new_distance > best_distance):
                    best_distance = new_distance
                    best_thetas = (new_theta1, new_theta2)
        
        # Update if we found a better extremum
        if best_thetas != (current_theta1, current_theta2):
            current_theta1, current_theta2 = best_thetas
        else:
            # If no improvement, reduce step size and try again
            step_size /= 2
            
            # If step size becomes too small, stop
            if step_size < 1e-6:
                break
    
    return current_theta1, current_theta2

def create_empty_in_collection(name: str, collection: Any, location: Tuple[float, float, float] = (0, 0, 0), 
                              empty_type: str = 'PLAIN_AXES', size: float = 0.2) -> Any:
    """Create an empty object and add it to the specified collection."""
    # Create the empty object
    bpy.ops.object.empty_add(type=empty_type, location=location)
    empty = bpy.context.active_object
    empty.name = name
    empty.empty_display_size = size
    
    # Move it to the correct collection
    bpy.context.collection.objects.unlink(empty)
    collection.objects.link(empty)
    
    return empty

def create_distance_indicators(planet1: str, planet2: str, sun_obj: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    """Create the distance indicator empties with proper parenting."""
    # Create master empty for organizing the distance indicators
    master_empty = create_empty_in_collection(
        f"{planet1}_{planet2}", 
        distances_collection, 
        empty_type='PLAIN_AXES', 
        size=0.4
    )
    master_empty.parent = sun_obj

    # Create parent empties for min and max under the master empty
    parent_min = create_empty_in_collection(
        f"{planet1}_{planet2}.min", 
        distances_collection, 
        empty_type='PLAIN_AXES', 
        size=0.3
    )
    parent_max = create_empty_in_collection(
        f"{planet1}_{planet2}.max", 
        distances_collection, 
        empty_type='PLAIN_AXES', 
        size=0.3
    )
    parent_min.parent = master_empty
    parent_max.parent = master_empty

    # Create empties for point markers
    p1_min_empty = create_empty_in_collection(
        f"{planet1}.min", 
        distances_collection, 
        location=result['min_point1'], 
        empty_type='SPHERE', 
        size=0.15
    )
    p1_max_empty = create_empty_in_collection(
        f"{planet1}.max", 
        distances_collection, 
        location=result['max_point1'], 
        empty_type='SPHERE', 
        size=0.15
    )
    p2_min_empty = create_empty_in_collection(
        f"{planet2}.min", 
        distances_collection, 
        location=result['min_point2'], 
        empty_type='SPHERE', 
        size=0.15
    )
    p2_max_empty = create_empty_in_collection(
        f"{planet2}.max", 
        distances_collection, 
        location=result['max_point2'], 
        empty_type='SPHERE', 
        size=0.15
    )

    # Parent the point empties to their respective min/max parent empties
    p1_min_empty.parent = parent_min
    p2_min_empty.parent = parent_min
    p1_max_empty.parent = parent_max
    p2_max_empty.parent = parent_max
    
    # Return a summary of the distance results
    return {
        'pair': f"{planet1}-{planet2}",
        'min_distance': result['min_distance'],
        'max_distance': result['max_distance']
    }

# Create Sun in Orbits collection
sun_orbits = create_empty_in_collection('Sun_orbits', orbits_collection, empty_type='PLAIN_AXES', size=0.5)

# Create Sun in Distances collection (for parenting distance indicators)
sun_distances = create_empty_in_collection('Sun_distances', distances_collection, empty_type='PLAIN_AXES', size=0.5)

# Add 1 AU reference circle
reference_data = {
    'a': 1.0,          # 1 AU
    'e': 0.0,          # perfect circle
    'inc': 0.0,        # no inclination
    'node': 0.0,       # no node rotation
    'peri': 0.0        # no perihelion argument
}
reference_orbit = create_orbital_curve('Reference', reference_data, 0, sun_orbits)

# Create orbits and store references to them
planet_orbits = {}
planet_order = ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres', 'Eros', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
for index, planet_name in enumerate(planet_order, 1):
    orbit = create_orbital_curve(planet_name, planets[planet_name], index, sun_orbits)
    planet_orbits[planet_name] = orbit

# Process each planet pair
distance_results = []
for planet1, planet2 in planet_pairs:
    print(f"Calculating distances between {planet1} and {planet2}...")
    
    # Find minimum and maximum distances
    result = find_min_max_distance_points(planet1, planet2)
    
    # Create distance indicators for this pair
    summary = create_distance_indicators(planet1, planet2, sun_distances, result)
    distance_results.append(summary)
    
    # Print results
    print(f"  Minimum distance: {result['min_distance']:.6f} AU")
    print(f"  Maximum distance: {result['max_distance']:.6f} AU")

# Print summary table of all results
print("\n=== Orbital Distance Summary ===")
print("Pair               Min (AU)    Max (AU)    Ratio (Max/Min)")
print("----------------------------------------------------------")
for res in distance_results:
    ratio = res['max_distance'] / res['min_distance']
    print(f"{res['pair']:<17} {res['min_distance']:10.6f} {res['max_distance']:10.6f} {ratio:10.2f}")

# Print execution time
end_time = time.time()
print(f"\nExecution time: {end_time - start_time:.2f} seconds")