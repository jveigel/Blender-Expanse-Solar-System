import bpy # type: ignore
import math
import numpy as np

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
    'Neptune': {'a': 30.068963, 'e': 0.008676, 'inc': 1.770, 'node': 131.783, 'peri': 273.187}
}

def create_orbital_curve(planet_name, data, index, parent_object):
    # Create the curve
    curve_data = bpy.data.curves.new(name=f"{index}.{planet_name}.Orbit", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 64
    curve_object = bpy.data.objects.new(f"{index}.{planet_name}.Orbit", curve_data)
    
    # Link it to the scene and parent to Sun
    bpy.context.scene.collection.objects.link(curve_object)
    curve_object.parent = parent_object
    
    # Create the orbital path
    spline = curve_data.splines.new('NURBS')
    
    # Calculate points along the orbit
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Get orbital parameters
    a = data['a']
    e = data['e']
    inc = math.radians(data['inc'])
    node = math.radians(data['node'])
    peri = math.radians(data['peri'])
    
    # Calculate points
    points = []
    for t in theta:
        # Calculate radius using polar form of ellipse
        r = a * (1 - e**2) / (1 + e * np.cos(t))
        
        # Initial position in orbital plane
        x = r * np.cos(t)
        y = r * np.sin(t)
        z = 0
        
        # Apply rotations in correct order: peri → inc → node
        # 1. Rotate by perihelion
        x_peri = x * np.cos(peri) - y * np.sin(peri)
        y_peri = x * np.sin(peri) + y * np.cos(peri)
        z_peri = z
        
        # 2. Rotate by inclination
        y_inc = y_peri * np.cos(inc) - z_peri * np.sin(inc)
        z_inc = y_peri * np.sin(inc) + z_peri * np.cos(inc)
        
        # 3. Rotate by node
        x_final = x_peri * np.cos(node) - y_inc * np.sin(node)
        y_final = x_peri * np.sin(node) + y_inc * np.cos(node)
        z_final = z_inc
        
        points.append((x_final, y_final, z_final))
    
    # Set the points in the spline
    spline.points.add(len(points)-1)
    for i, point in enumerate(points):
        spline.points[i].co = (point[0], point[1], point[2], 1)
    
    # Close the curve
    spline.use_cyclic_u = True
    
    return curve_object

# Create Sun at center
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
sun = bpy.context.active_object
sun.name = 'Sun'
sun.empty_display_size = 0.5

# Create orbits
planet_order = ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres', 'Eros', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
for index, planet_name in enumerate(planet_order, 1):
    orbit = create_orbital_curve(planet_name, planets[planet_name], index, sun)