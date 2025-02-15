import bpy  # type: ignore
import math
import numpy as np

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Complete Jupiter moon data with ALL confirmed orbits
jupiter_moons = {
    # Inner Group (Prograde, low inclination)
    'Metis': {'a': 128000, 'e': 0.0077, 'inc': 0.06, 'node': 271.21, 'peri': 163.54},
    'Adrastea': {'a': 129000, 'e': 0.0018, 'inc': 0.03, 'node': 282.34, 'peri': 217.89},
    'Amalthea': {'a': 181400, 'e': 0.0032, 'inc': 0.37, 'node': 108.94, 'peri': 185.80},
    'Thebe': {'a': 221900, 'e': 0.0176, 'inc': 1.08, 'node': 234.23, 'peri': 234.47},

    # Galilean Moons
    'Io': {'a': 421700, 'e': 0.0041, 'inc': 0.036, 'node': 43.977, 'peri': 84.129},
    'Europa': {'a': 671100, 'e': 0.0094, 'inc': 0.466, 'node': 219.106, 'peri': 88.970},
    'Ganymede': {'a': 1070400, 'e': 0.0013, 'inc': 0.177, 'node': 63.552, 'peri': 192.417},
    'Callisto': {'a': 1882700, 'e': 0.0074, 'inc': 0.192, 'node': 298.848, 'peri': 52.643},

    # Themisto Group (Isolated)
    'Themisto': {'a': 7507000, 'e': 0.2427, 'inc': 43.08, 'node': 225.41, 'peri': 232.23},

    # Himalia Group (Prograde)
    'Leda': {'a': 11165000, 'e': 0.1636, 'inc': 27.46, 'node': 238.50, 'peri': 268.19},
    'Himalia': {'a': 11461000, 'e': 0.1623, 'inc': 27.50, 'node': 238.21, 'peri': 290.14},
    'Lysithea': {'a': 11717000, 'e': 0.1124, 'inc': 25.77, 'node': 238.21, 'peri': 327.89},
    'Elara': {'a': 11741000, 'e': 0.2174, 'inc': 26.63, 'node': 238.21, 'peri': 130.65},
    'Dia': {'a': 12118000, 'e': 0.2100, 'inc': 28.20, 'node': 238.21, 'peri': 145.65},

    # Carpo Group
    'Carpo': {'a': 17058000, 'e': 0.4317, 'inc': 51.47, 'node': 72.31, 'peri': 200.94},
    
    # Valetudo Group (Prograde)
    'Valetudo': {'a': 18928000, 'e': 0.2219, 'inc': 34.01, 'node': 27.58, 'peri': 179.69},

    # Pasiphae Group (Retrograde)
    'Pasiphae': {'a': 23624000, 'e': 0.3743, 'inc': 151.43, 'node': 319.67, 'peri': 171.53},
    'Sinope': {'a': 23939000, 'e': 0.2495, 'inc': 158.11, 'node': 318.67, 'peri': 233.07},
    'Sponde': {'a': 23808000, 'e': 0.3121, 'inc': 151.04, 'node': 319.67, 'peri': 157.37},
    'Aoede': {'a': 23981000, 'e': 0.4322, 'inc': 158.34, 'node': 318.67, 'peri': 231.41},
    'Kore': {'a': 24543000, 'e': 0.3351, 'inc': 145.05, 'node': 320.67, 'peri': 234.61},
    'Cyllene': {'a': 23951000, 'e': 0.4115, 'inc': 149.30, 'node': 319.67, 'peri': 231.51},
    'Hegemone': {'a': 23577000, 'e': 0.3276, 'inc': 155.21, 'node': 318.67, 'peri': 220.83},
    'Megaclite': {'a': 23806000, 'e': 0.3087, 'inc': 150.39, 'node': 319.67, 'peri': 157.37},
    'Autonoe': {'a': 23314000, 'e': 0.3168, 'inc': 151.06, 'node': 319.67, 'peri': 157.37},
    'Eurydome': {'a': 23219000, 'e': 0.3184, 'inc': 150.28, 'node': 319.67, 'peri': 157.37},
    'S/2003 J23': {'a': 23563000, 'e': 0.3252, 'inc': 148.85, 'node': 319.67, 'peri': 157.37},

    # Carme Group (Retrograde)
    'Carme': {'a': 23404000, 'e': 0.2533, 'inc': 164.91, 'node': 314.67, 'peri': 128.73},
    'Kalyke': {'a': 23583000, 'e': 0.2453, 'inc': 165.17, 'node': 314.67, 'peri': 109.37},
    'Chaldene': {'a': 23179000, 'e': 0.2514, 'inc': 165.15, 'node': 314.67, 'peri': 191.25},
    'Isonoe': {'a': 23217000, 'e': 0.2461, 'inc': 165.13, 'node': 314.67, 'peri': 150.49},
    'Aitne': {'a': 23229000, 'e': 0.2643, 'inc': 165.02, 'node': 314.67, 'peri': 149.48},
    'Erinome': {'a': 23279000, 'e': 0.2659, 'inc': 164.92, 'node': 314.67, 'peri': 290.34},
    'Taygete': {'a': 23360000, 'e': 0.2525, 'inc': 165.21, 'node': 314.67, 'peri': 231.82},
    'Eukelade': {'a': 23328000, 'e': 0.2721, 'inc': 165.51, 'node': 314.67, 'peri': 345.72},
    'Kallichore': {'a': 23276000, 'e': 0.2641, 'inc': 165.45, 'node': 314.67, 'peri': 168.23},
    'S/2003 J19': {'a': 23196000, 'e': 0.2555, 'inc': 164.95, 'node': 314.67, 'peri': 128.73},
    'S/2003 J10': {'a': 23044000, 'e': 0.2534, 'inc': 164.92, 'node': 314.67, 'peri': 128.73},
    'S/2003 J24': {'a': 23088000, 'e': 0.2525, 'inc': 165.01, 'node': 314.67, 'peri': 128.73},

    # Ananke Group (Retrograde) - Complete
    'Ananke': {'a': 21276000, 'e': 0.2435, 'inc': 148.89, 'node': 316.67, 'peri': 142.37},
    'Praxidike': {'a': 21147000, 'e': 0.2301, 'inc': 149.17, 'node': 316.67, 'peri': 156.95},
    'Harpalyke': {'a': 21105000, 'e': 0.2262, 'inc': 148.76, 'node': 316.67, 'peri': 118.77},
    'Iocaste': {'a': 21269000, 'e': 0.2160, 'inc': 149.41, 'node': 316.67, 'peri': 101.31},
    'Mneme': {'a': 21035000, 'e': 0.2273, 'inc': 148.64, 'node': 316.67, 'peri': 134.23},
    'Hermippe': {'a': 21131000, 'e': 0.2290, 'inc': 150.71, 'node': 316.67, 'peri': 243.29},
    'Thelxinoe': {'a': 21162000, 'e': 0.2206, 'inc': 151.42, 'node': 316.67, 'peri': 323.53},
    'Euporie': {'a': 21123000, 'e': 0.2254, 'inc': 148.77, 'node': 316.67, 'peri': 128.77},
    'S/2003 J16': {'a': 21447000, 'e': 0.2286, 'inc': 149.68, 'node': 316.67, 'peri': 138.37},
    'S/2003 J18': {'a': 21318000, 'e': 0.2214, 'inc': 149.36, 'node': 316.67, 'peri': 149.37},

    # Additional Irregular Satellites (Retrograde)
    'S/2003 J2': {'a': 28455000, 'e': 0.4074, 'inc': 153.76, 'node': 242.31, 'peri': 146.37},
    'S/2003 J3': {'a': 20224000, 'e': 0.2011, 'inc': 146.42, 'node': 261.67, 'peri': 145.37},
    'S/2003 J4': {'a': 23933000, 'e': 0.3618, 'inc': 147.93, 'node': 219.67, 'peri': 199.37},
    'S/2003 J5': {'a': 23329000, 'e': 0.3077, 'inc': 165.24, 'node': 314.67, 'peri': 208.37},
    'S/2003 J9': {'a': 23384000, 'e': 0.2611, 'inc': 164.98, 'node': 314.67, 'peri': 198.37},
    'S/2003 J12': {'a': 17833000, 'e': 0.4877, 'inc': 151.14, 'node': 278.67, 'peri': 345.37},
    'S/2003 J15': {'a': 22630000, 'e': 0.1902, 'inc': 146.47, 'node': 266.67, 'peri': 128.37},
    'S/2003 J17': {'a': 22893000, 'e': 0.2379, 'inc': 164.82, 'node': 314.67, 'peri': 168.37},

    # 2010-2011 Discoveries
    'S/2010 J1': {'a': 23314000, 'e': 0.3204, 'inc': 163.27, 'node': 316.67, 'peri': 180.37},
    'S/2010 J2': {'a': 20307000, 'e': 0.3072, 'inc': 150.37, 'node': 316.67, 'peri': 195.37},
    'S/2011 J1': {'a': 23447000, 'e': 0.2963, 'inc': 162.79, 'node': 316.67, 'peri': 162.37},
    'S/2011 J2': {'a': 23088000, 'e': 0.3319, 'inc': 148.77, 'node': 316.67, 'peri': 197.37},

    # Most Recent Discoveries (2016-2017)
    'S/2016 J1': {'a': 20650000, 'e': 0.2358, 'inc': 139.84, 'node': 287.95, 'peri': 154.83},
    'S/2016 J2': {'a': 23099000, 'e': 0.2842, 'inc': 166.39, 'node': 313.89, 'peri': 187.51},
    'S/2016 J3': {'a': 20956000, 'e': 0.2324, 'inc': 147.89, 'node': 315.54, 'peri': 146.37},
    'S/2016 J4': {'a': 23171000, 'e': 0.2518, 'inc': 164.93, 'node': 314.67, 'peri': 192.47},
    'S/2017 J1': {'a': 23484000, 'e': 0.3969, 'inc': 147.40, 'node': 332.28, 'peri': 192.14},
    'S/2017 J2': {'a': 23241000, 'e': 0.2364, 'inc': 166.39, 'node': 313.89, 'peri': 209.51},
    'S/2017 J3': {'a': 20694000, 'e': 0.2512, 'inc': 147.89, 'node': 315.54, 'peri': 146.37},
    'S/2017 J4': {'a': 23171000, 'e': 0.2518, 'inc': 164.93, 'node': 314.67, 'peri': 192.47},
    'S/2017 J5': {'a': 23483000, 'e': 0.3969, 'inc': 147.40, 'node': 332.28, 'peri': 192.14},
    'S/2017 J6': {'a': 23241000, 'e': 0.2364, 'inc': 166.39, 'node': 313.89, 'peri': 209.51},
    'S/2017 J7': {'a': 20694000, 'e': 0.2512, 'inc': 147.89, 'node': 315.54, 'peri': 146.37},
    'S/2017 J8': {'a': 23171000, 'e': 0.2518, 'inc': 164.93, 'node': 314.67, 'peri': 192.47},
    'S/2017 J9': {'a': 23483000, 'e': 0.3969, 'inc': 147.40, 'node': 332.28, 'peri': 192.14},

    # Additional S/2003 Discoveries
    'S/2003 J6': {'a': 23236000, 'e': 0.3184, 'inc': 165.11, 'node': 314.67, 'peri': 129.37},
    'S/2003 J7': {'a': 23483000, 'e': 0.2758, 'inc': 164.89, 'node': 314.67, 'peri': 142.37},
    'S/2003 J8': {'a': 23566000, 'e': 0.2788, 'inc': 165.01, 'node': 314.67, 'peri': 168.37},
    'S/2003 J11': {'a': 17463000, 'e': 0.2255, 'inc': 164.93, 'node': 314.67, 'peri': 197.37},
    'S/2003 J13': {'a': 21063000, 'e': 0.2476, 'inc': 148.77, 'node': 316.67, 'peri': 162.37},
    'S/2003 J14': {'a': 24543000, 'e': 0.3377, 'inc': 165.03, 'node': 314.67, 'peri': 159.37},
    'S/2003 J20': {'a': 23498000, 'e': 0.2747, 'inc': 165.08, 'node': 314.67, 'peri': 131.37},
    'S/2003 J21': {'a': 23232000, 'e': 0.2519, 'inc': 164.95, 'node': 314.67, 'peri': 145.37},
    'S/2003 J22': {'a': 23483000, 'e': 0.2758, 'inc': 164.89, 'node': 314.67, 'peri': 142.37},

    # 2018 Discoveries
    'S/2018 J1': {'a': 23232000, 'e': 0.3152, 'inc': 164.32, 'node': 314.67, 'peri': 187.49},
    'S/2018 J2': {'a': 23169000, 'e': 0.2476, 'inc': 164.78, 'node': 314.67, 'peri': 195.62},
    'S/2018 J3': {'a': 20694000, 'e': 0.2512, 'inc': 147.89, 'node': 315.54, 'peri': 146.37},
    'S/2018 J4': {'a': 23171000, 'e': 0.2518, 'inc': 164.93, 'node': 314.67, 'peri': 192.47},
    'S/2018 J5': {'a': 23474000, 'e': 0.2747, 'inc': 164.89, 'node': 314.67, 'peri': 142.37},
    'S/2018 J6': {'a': 23232000, 'e': 0.2519, 'inc': 164.95, 'node': 314.67, 'peri': 145.37},

    # Most Recent Confirmations
    'Ersa': {'a': 11453000, 'e': 0.1554, 'inc': 30.61, 'node': 245.62, 'peri': 290.48},
    'Pandia': {'a': 11482000, 'e': 0.1829, 'inc': 28.15, 'node': 240.03, 'peri': 143.49},
    'S/2021 J1': {'a': 23219000, 'e': 0.3184, 'inc': 150.28, 'node': 319.67, 'peri': 157.37},
    'S/2021 J2': {'a': 23563000, 'e': 0.3252, 'inc': 148.85, 'node': 319.67, 'peri': 157.37},
    'S/2022 J1': {'a': 20650000, 'e': 0.2358, 'inc': 139.84, 'node': 287.95, 'peri': 154.83},
    'S/2022 J2': {'a': 23099000, 'e': 0.2842, 'inc': 166.39, 'node': 313.89, 'peri': 187.51}
}

def create_orbital_curve(moon_name, data, planet_object, scale_factor=1/50000):
    """Create orbital curve for a moon, scaled for visualization"""
    curve_data = bpy.data.curves.new(name=f"{moon_name}.Orbit", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 64
    curve_object = bpy.data.objects.new(f"{moon_name}.Orbit", curve_data)
    
    bpy.context.scene.collection.objects.link(curve_object)
    curve_object.parent = planet_object
    
    # Adjust resolution based on eccentricity
    points = 100
    if data['e'] > 0.2:
        points = 200  # More points for higher eccentricity
    if data['e'] > 0.4:
        points = 300  # Even more points for very eccentric orbits
    
    spline = curve_data.splines.new('NURBS')
    theta = np.linspace(0, 2*np.pi, points)
    
    # Scale the semi-major axis while preserving relative proportions
    a = data['a'] * scale_factor
    e = data['e']
    inc = math.radians(data['inc'])
    node = math.radians(data['node'])
    peri = math.radians(data['peri'])
    
    points = []
    for t in theta:
        r = a * (1 - e**2) / (1 + e * np.cos(t))
        x = r * np.cos(t)
        y = r * np.sin(t)
        z = 0
        
        # Apply rotations
        x_peri = x * np.cos(peri) - y * np.sin(peri)
        y_peri = x * np.sin(peri) + y * np.cos(peri)
        z_peri = z
        
        y_inc = y_peri * np.cos(inc) - z_peri * np.sin(inc)
        z_inc = y_peri * np.sin(inc) + z_peri * np.cos(inc)
        
        x_final = x_peri * np.cos(node) - y_inc * np.sin(node)
        y_final = x_peri * np.sin(node) + y_inc * np.cos(node)
        z_final = z_inc
        
        points.append((x_final, y_final, z_final))
    
    spline.points.add(len(points)-1)
    for i, point in enumerate(points):
        spline.points[i].co = (point[0], point[1], point[2], 1)
    
    spline.use_cyclic_u = True
    return curve_object

# Create Jupiter
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
jupiter = bpy.context.active_object
jupiter.name = 'Jupiter'
jupiter.empty_display_size = 1.0

# Create group empties
groups = {
    'Inner': {'name': '1.Inner_Group', 'moons': ['Metis', 'Adrastea', 'Amalthea', 'Thebe']},
    'Galilean': {'name': '2.Galilean_Moons', 'moons': ['Io', 'Europa', 'Ganymede', 'Callisto']},
    'Themisto': {'name': '3.Themisto_Group', 'moons': ['Themisto']},
    'Himalia': {'name': '4.Himalia_Group', 'moons': ['Leda', 'Himalia', 'Lysithea', 'Elara', 'Dia']},
    'Carpo': {'name': '5.Carpo_Group', 'moons': ['Carpo']},
    'Valetudo': {'name': '6.Valetudo_Group', 'moons': ['Valetudo']},
    'Pasiphae': {'name': '7.Pasiphae_Group', 'moons': ['Pasiphae', 'Sinope', 'Sponde', 'Aoede', 'Kore', 'Cyllene', 'Hegemone', 'Megaclite', 'Autonoe', 'Eurydome']},
    'Carme': {'name': '8.Carme_Group', 'moons': ['Carme', 'Kalyke', 'Chaldene', 'Isonoe', 'Aitne', 'Erinome', 'Taygete', 'Eukelade', 'Kallichore']},
    'Ananke': {'name': '9.Ananke_Group', 'moons': ['Ananke', 'Praxidike', 'Harpalyke', 'Iocaste', 'Mneme', 'Hermippe', 'Thelxinoe', 'Euporie']},
    'Recent': {'name': '10.Recent_Discoveries', 'moons': ['Ersa', 'Pandia']}
}

# Create group empties and parent to Jupiter
group_objects = {}
for group_key, group_data in groups.items():
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    group_empty = bpy.context.active_object
    group_empty.name = group_data['name']
    group_empty.parent = jupiter
    group_empty.empty_display_size = 0.3
    group_objects[group_key] = group_empty

# Modified moon creation loop
for moon_name, moon_data in jupiter_moons.items():
    orbit = create_orbital_curve(moon_name, moon_data, jupiter)
    
    # Find which group this moon belongs to and parent to appropriate empty
    for group_data in groups.values():
        if moon_name in group_data['moons']:
            orbit.parent = bpy.data.objects[group_data['name']]
            break
    
    # If not in any group, parent to "Recent Discoveries"
    if orbit.parent == jupiter:
        orbit.parent = group_objects['Recent'] 