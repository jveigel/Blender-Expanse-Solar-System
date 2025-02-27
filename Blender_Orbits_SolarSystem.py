import bpy # type: ignore
import math
import numpy as np
from mathutils import Vector

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

NUM_POINTS = 500  # Balance between accuracy and speed

def calculate_point_on_orbit(data, true_anomaly):
    """Calculate 3D position at a given true anomaly."""
    # Get orbital parameters
    a = data['a']
    e = data['e']
    inc = math.radians(data['inc'])
    node = math.radians(data['node'])
    peri = math.radians(data['peri'])
    
    # Calculate radius using polar form of ellipse
    r = a * (1 - e**2) / (1 + e * math.cos(true_anomaly))
    
    # Initial position in orbital plane
    x = r * math.cos(true_anomaly)
    y = r * math.sin(true_anomaly)
    z = 0
    
    # Apply rotations in correct order: peri → inc → node
    # 1. Rotate by perihelion
    x_peri = x * math.cos(peri) - y * math.sin(peri)
    y_peri = x * math.sin(peri) + y * math.cos(peri)
    z_peri = z
    
    # 2. Rotate by inclination
    y_inc = y_peri * math.cos(inc) - z_peri * math.sin(inc)
    z_inc = y_peri * math.sin(inc) + z_peri * math.cos(inc)
    
    # 3. Rotate by node
    x_final = x_peri * math.cos(node) - y_inc * math.sin(node)
    y_final = x_peri * math.sin(node) + y_inc * math.cos(node)
    z_final = z_inc
    
    return Vector((x_final, y_final, z_final))

# Create collections for organization
def setup_collections():
    """Set up the collections structure."""
    # Get scene collection
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

def create_orbital_curve(planet_name, data, index, parent_object):
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
    
    # Calculate points along the orbit
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Calculate points
    points = []
    for t in theta:
        point = calculate_point_on_orbit(data, t)
        points.append(point)
    
    # Set the points in the spline
    spline.points.add(len(points)-1)
    for i, point in enumerate(points):
        spline.points[i].co = (point[0], point[1], point[2], 1)
    
    # Close the curve
    spline.use_cyclic_u = True
    
    return curve_object

def find_min_max_distance_points(planet1_data, planet2_data):
    """Find the points of minimum and maximum distance between two orbits."""
    # Sample points along both orbits
    theta_values = np.linspace(0, 2*np.pi, NUM_POINTS)
    
    orbit1_points = [calculate_point_on_orbit(planet1_data, t) for t in theta_values]
    orbit2_points = [calculate_point_on_orbit(planet2_data, t) for t in theta_values]
    
    # Calculate distances between all pairs of points
    min_distance = float('inf')
    max_distance = 0
    min_point1 = None
    min_point2 = None
    max_point1 = None
    max_point2 = None
    min_theta1 = min_theta2 = max_theta1 = max_theta2 = 0
    
    # For better performance, we could optimize this with numpy operations
    # But the direct approach is more readable
    for i, point1 in enumerate(orbit1_points):
        for j, point2 in enumerate(orbit2_points):
            distance = (point1 - point2).length
            
            if distance < min_distance:
                min_distance = distance
                min_point1 = point1
                min_point2 = point2
                min_theta1 = theta_values[i]
                min_theta2 = theta_values[j]
                
            if distance > max_distance:
                max_distance = distance
                max_point1 = point1
                max_point2 = point2
                max_theta1 = theta_values[i]
                max_theta2 = theta_values[j]
    
    # Refine the search around the approximate minimum and maximum
    # This uses a simple gradient descent approach to get more precise points
    min_theta1, min_theta2 = refine_extremum(planet1_data, planet2_data, min_theta1, min_theta2, is_minimum=True)
    max_theta1, max_theta2 = refine_extremum(planet1_data, planet2_data, max_theta1, max_theta2, is_minimum=False)
    
    # Recalculate the points with refined angles
    min_point1 = calculate_point_on_orbit(planet1_data, min_theta1)
    min_point2 = calculate_point_on_orbit(planet2_data, min_theta2)
    max_point1 = calculate_point_on_orbit(planet1_data, max_theta1)
    max_point2 = calculate_point_on_orbit(planet2_data, max_theta2)
    
    # Calculate final distances
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

def refine_extremum(planet1_data, planet2_data, theta1, theta2, is_minimum=True, steps=5, step_size=0.001):
    """Refine the extremum point using gradient descent."""
    current_theta1 = theta1
    current_theta2 = theta2
    
    for _ in range(steps):
        # Calculate current distance
        p1 = calculate_point_on_orbit(planet1_data, current_theta1)
        p2 = calculate_point_on_orbit(planet2_data, current_theta2)
        current_distance = (p1 - p2).length
        
        # Try small steps in each direction
        distances = []
        theta_pairs = []
        
        for dt1 in [-step_size, 0, step_size]:
            for dt2 in [-step_size, 0, step_size]:
                if dt1 == 0 and dt2 == 0:
                    continue
                
                new_theta1 = (current_theta1 + dt1) % (2*math.pi)
                new_theta2 = (current_theta2 + dt2) % (2*math.pi)
                
                p1_new = calculate_point_on_orbit(planet1_data, new_theta1)
                p2_new = calculate_point_on_orbit(planet2_data, new_theta2)
                new_distance = (p1_new - p2_new).length
                
                distances.append(new_distance)
                theta_pairs.append((new_theta1, new_theta2))
        
        # Find the best step
        if is_minimum:
            best_idx = np.argmin(distances)
        else:
            best_idx = np.argmax(distances)
        
        # Update if we found a better extremum
        if (is_minimum and distances[best_idx] < current_distance) or \
           (not is_minimum and distances[best_idx] > current_distance):
            current_theta1, current_theta2 = theta_pairs[best_idx]
        else:
            # If no improvement, reduce step size and try again
            step_size /= 2
            
            # If step size becomes too small, stop
            if step_size < 1e-6:
                break
    
    return current_theta1, current_theta2

def create_empty_in_collection(name, collection, location=(0, 0, 0), empty_type='PLAIN_AXES', size=0.2):
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

def create_distance_indicators(planet1, planet2, sun_obj, result):
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
    result = find_min_max_distance_points(planets[planet1], planets[planet2])
    
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