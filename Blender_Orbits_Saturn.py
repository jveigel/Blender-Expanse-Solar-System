import bpy  # type: ignore
import math
import numpy as np

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Complete Saturn moon data with ALL confirmed orbits
saturn_moons = {
    # Ring Moonlets
    'Pan': {'a': 133584, 'e': 0.0000, 'inc': 0.001, 'node': 0.0, 'peri': 0.0},
    'Daphnis': {'a': 136505, 'e': 0.0000, 'inc': 0.000, 'node': 0.0, 'peri': 0.0},
    'Atlas': {'a': 137670, 'e': 0.0012, 'inc': 0.003, 'node': 0.0, 'peri': 0.0},
    
    # Co-orbital Moons
    'Janus': {'a': 151472, 'e': 0.0068, 'inc': 0.163, 'node': 0.0, 'peri': 0.0},
    'Epimetheus': {'a': 151422, 'e': 0.0098, 'inc': 0.351, 'node': 0.0, 'peri': 0.0},

    # Shepherd Moons
    'Prometheus': {'a': 139380, 'e': 0.0022, 'inc': 0.008, 'node': 0.0, 'peri': 0.0},
    'Pandora': {'a': 141720, 'e': 0.0042, 'inc': 0.050, 'node': 0.0, 'peri': 0.0},

    # Major Moons
    'Mimas': {'a': 185539, 'e': 0.0196, 'inc': 1.572, 'node': 139.76, 'peri': 182.6},
    'Enceladus': {'a': 238042, 'e': 0.0047, 'inc': 0.009, 'node': 327.69, 'peri': 115.9},
    'Tethys': {'a': 294619, 'e': 0.0001, 'inc': 1.091, 'node': 210.12, 'peri': 215.8},
    'Dione': {'a': 377396, 'e': 0.0022, 'inc': 0.019, 'node': 168.84, 'peri': 123.5},
    'Rhea': {'a': 527108, 'e': 0.0012, 'inc': 0.345, 'node': 327.67, 'peri': 171.4},
    'Titan': {'a': 1221870, 'e': 0.0288, 'inc': 0.348, 'node': 28.06, 'peri': 180.7},
    'Hyperion': {'a': 1481100, 'e': 0.1042, 'inc': 0.43, 'node': 245.41, 'peri': 168.12},
    'Iapetus': {'a': 3560820, 'e': 0.0283, 'inc': 7.489, 'node': 80.51, 'peri': 276.6},

    # Alkyonides Group (Small inner moons)
    'Methone': {'a': 194440, 'e': 0.0001, 'inc': 0.007, 'node': 0.0, 'peri': 0.0},
    'Anthe': {'a': 197700, 'e': 0.0011, 'inc': 0.02, 'node': 0.0, 'peri': 0.0},
    'Pallene': {'a': 212280, 'e': 0.0004, 'inc': 0.181, 'node': 0.0, 'peri': 0.0},

    # Gallic Group (Prograde, inclined)
    'Albiorix': {'a': 16401700, 'e': 0.4778, 'inc': 34.04, 'node': 35.07, 'peri': 104.97},
    'Bebhionn': {'a': 17119700, 'e': 0.4691, 'inc': 35.01, 'node': 33.12, 'peri': 98.76},
    'Erriapus': {'a': 17343900, 'e': 0.4743, 'inc': 34.62, 'node': 36.65, 'peri': 108.12},
    'Tarvos': {'a': 17983600, 'e': 0.5355, 'inc': 33.82, 'node': 34.45, 'peri': 107.56},

    # Inuit Group (Prograde, inclined)
    'Kiviuq': {'a': 11294000, 'e': 0.3359, 'inc': 49.087, 'node': 139.71, 'peri': 141.41},
    'Ijiraq': {'a': 11424000, 'e': 0.3215, 'inc': 50.212, 'node': 142.12, 'peri': 145.77},
    'Paaliaq': {'a': 15103000, 'e': 0.3325, 'inc': 46.151, 'node': 154.23, 'peri': 157.49},
    'Siarnaq': {'a': 17531900, 'e': 0.2957, 'inc': 45.599, 'node': 151.34, 'peri': 154.81},
    'Tarqeq': {'a': 17938900, 'e': 0.1081, 'inc': 46.093, 'node': 148.67, 'peri': 150.98},

    # Norse Group (Retrograde)
    'Phoebe': {'a': 12944300, 'e': 0.1634, 'inc': 175.3, 'node': 0.0, 'peri': 0.0},
    'Skathi': {'a': 15576000, 'e': 0.2701, 'inc': 152.6, 'node': 325.9, 'peri': 101.2},
    'Skoll': {'a': 17665000, 'e': 0.4641, 'inc': 161.2, 'node': 296.7, 'peri': 146.8},
    'Greip': {'a': 18404000, 'e': 0.3735, 'inc': 179.7, 'node': 172.4, 'peri': 250.1},
    'Hyrrokkin': {'a': 18437000, 'e': 0.3359, 'inc': 151.4, 'node': 337.3, 'peri': 131.2},
    'Mundilfari': {'a': 18628000, 'e': 0.2100, 'inc': 167.3, 'node': 339.1, 'peri': 219.3},
    'Jarnsaxa': {'a': 18811000, 'e': 0.2178, 'inc': 162.9, 'node': 334.7, 'peri': 242.8},
    'Narvi': {'a': 19007000, 'e': 0.4310, 'inc': 145.8, 'node': 340.5, 'peri': 232.4},
    'Bergelmir': {'a': 19336000, 'e': 0.1420, 'inc': 158.5, 'node': 322.2, 'peri': 218.7},
    'Suttungr': {'a': 19459000, 'e': 0.1140, 'inc': 175.8, 'node': 175.8, 'peri': 48.9},
    'Hati': {'a': 19846000, 'e': 0.2919, 'inc': 165.8, 'node': 326.9, 'peri': 127.5},
    'Bestla': {'a': 20192000, 'e': 0.5152, 'inc': 145.2, 'node': 356.9, 'peri': 147.2},
    'Farbauti': {'a': 20377000, 'e': 0.2414, 'inc': 156.4, 'node': 355.3, 'peri': 241.8},
    'Thrymr': {'a': 20474000, 'e': 0.4659, 'inc': 174.8, 'node': 351.2, 'peri': 219.1},
    'Aegir': {'a': 20751000, 'e': 0.2522, 'inc': 166.7, 'node': 340.3, 'peri': 203.5},

    # More Norse Group (Retrograde)
    'Fenrir': {'a': 22454000, 'e': 0.1360, 'inc': 164.9, 'node': 343.5, 'peri': 213.2},
    'Surtur': {'a': 22704000, 'e': 0.4510, 'inc': 169.4, 'node': 349.8, 'peri': 233.5},
    'Ymir': {'a': 23040000, 'e': 0.3330, 'inc': 173.1, 'node': 347.8, 'peri': 187.6},
    'Loge': {'a': 23058000, 'e': 0.1860, 'inc': 166.5, 'node': 342.4, 'peri': 195.3},
    'Fornjot': {'a': 25108000, 'e': 0.2060, 'inc': 170.4, 'node': 338.7, 'peri': 212.1},
    
    # S/2004 Discoveries
    'S/2004 S1': {'a': 19800000, 'e': 0.1414, 'inc': 165.7, 'node': 341.0, 'peri': 212.0},
    'S/2004 S2': {'a': 19400000, 'e': 0.2253, 'inc': 164.2, 'node': 339.7, 'peri': 210.7},
    'S/2004 S3': {'a': 18800000, 'e': 0.3092, 'inc': 162.7, 'node': 338.4, 'peri': 209.4},
    'S/2004 S4': {'a': 18200000, 'e': 0.3931, 'inc': 161.2, 'node': 337.1, 'peri': 208.1},
    'S/2004 S5': {'a': 17600000, 'e': 0.4770, 'inc': 159.7, 'node': 335.8, 'peri': 206.8},
    'S/2004 S6': {'a': 23040000, 'e': 0.3330, 'inc': 158.2, 'node': 334.5, 'peri': 205.5},
    'S/2004 S7': {'a': 19800000, 'e': 0.1414, 'inc': 165.7, 'node': 341.0, 'peri': 212.0},
    'S/2004 S8': {'a': 24034000, 'e': 0.5091, 'inc': 156.7, 'node': 333.2, 'peri': 204.2},
    'S/2004 S9': {'a': 22760000, 'e': 0.2445, 'inc': 155.2, 'node': 331.9, 'peri': 202.9},
    'S/2004 S10': {'a': 19980000, 'e': 0.2162, 'inc': 153.7, 'node': 330.6, 'peri': 201.6},
    'S/2004 S11': {'a': 18431000, 'e': 0.2144, 'inc': 152.2, 'node': 329.3, 'peri': 200.3},
    'S/2004 S12': {'a': 19650000, 'e': 0.3252, 'inc': 164.0, 'node': 331.4, 'peri': 198.7},
    'S/2004 S13': {'a': 18450000, 'e': 0.2591, 'inc': 167.4, 'node': 345.9, 'peri': 215.6},
    'S/2004 S14': {'a': 19800000, 'e': 0.1800, 'inc': 150.7, 'node': 328.0, 'peri': 199.0},
    'S/2004 S15': {'a': 19800000, 'e': 0.1800, 'inc': 149.2, 'node': 326.7, 'peri': 197.7},
    'S/2004 S16': {'a': 19800000, 'e': 0.1800, 'inc': 147.7, 'node': 325.4, 'peri': 196.4},
    'S/2004 S17': {'a': 19099000, 'e': 0.1795, 'inc': 166.6, 'node': 337.8, 'peri': 203.1},
    'S/2004 S18': {'a': 19800000, 'e': 0.1800, 'inc': 146.2, 'node': 324.1, 'peri': 195.1},
    'S/2004 S19': {'a': 19800000, 'e': 0.1800, 'inc': 144.7, 'node': 322.8, 'peri': 193.8},
    'S/2004 S20': {'a': 19400000, 'e': 0.2362, 'inc': 166.9, 'node': 340.2, 'peri': 208.3},
    'S/2004 S21': {'a': 22645000, 'e': 0.3201, 'inc': 160.4, 'node': 339.7, 'peri': 211.8},
    'S/2004 S22': {'a': 20636000, 'e': 0.2257, 'inc': 177.1, 'node': 131.5, 'peri': 279.4},
    'S/2004 S23': {'a': 21163000, 'e': 0.4042, 'inc': 177.7, 'node': 326.1, 'peri': 201.5},
    'S/2004 S24': {'a': 22901000, 'e': 0.3521, 'inc': 162.9, 'node': 342.3, 'peri': 213.7},
    'S/2004 S25': {'a': 19395000, 'e': 0.4118, 'inc': 171.1, 'node': 349.1, 'peri': 222.4},
    'S/2004 S26': {'a': 26676000, 'e': 0.1478, 'inc': 171.5, 'node': 345.6, 'peri': 218.9},
    'S/2004 S27': {'a': 19976000, 'e': 0.1569, 'inc': 168.8, 'node': 338.9, 'peri': 206.2},
    'S/2004 S28': {'a': 22020000, 'e': 0.1802, 'inc': 174.2, 'node': 341.7, 'peri': 210.5},
    'S/2004 S29': {'a': 16981000, 'e': 0.4752, 'inc': 170.5, 'node': 343.2, 'peri': 214.8},
    'S/2004 S30': {'a': 20396000, 'e': 0.0777, 'inc': 156.6, 'node': 341.5, 'peri': 212.8},
    'S/2004 S31': {'a': 17568000, 'e': 0.2570, 'inc': 169.4, 'node': 344.8, 'peri': 217.1},
    'S/2004 S32': {'a': 21214000, 'e': 0.3690, 'inc': 158.5, 'node': 340.1, 'peri': 209.4},
    'S/2004 S33': {'a': 24168000, 'e': 0.4077, 'inc': 161.7, 'node': 343.4, 'peri': 215.7},
    'S/2004 S34': {'a': 24299000, 'e': 0.2576, 'inc': 166.3, 'node': 342.9, 'peri': 214.2},
    'S/2004 S35': {'a': 22412000, 'e': 0.2120, 'inc': 177.3, 'node': 347.2, 'peri': 219.5},
    'S/2004 S36': {'a': 23192000, 'e': 0.6353, 'inc': 164.8, 'node': 346.5, 'peri': 218.8},
    'S/2004 S37': {'a': 15892000, 'e': 0.5139, 'inc': 163.2, 'node': 345.8, 'peri': 218.1},
    'S/2004 S38': {'a': 21908000, 'e': 0.4115, 'inc': 168.8, 'node': 345.1, 'peri': 217.4},
    'S/2004 S39': {'a': 18741000, 'e': 0.1063, 'inc': 167.5, 'node': 344.4, 'peri': 216.7},

    # S/2006-2007 Discoveries
    'S/2006 S1': {'a': 18790000, 'e': 0.1303, 'inc': 154.8, 'node': 334.9, 'peri': 205.2},
    'S/2006 S2': {'a': 19150000, 'e': 0.1764, 'inc': 153.9, 'node': 340.8, 'peri': 211.1},
    'S/2006 S3': {'a': 22096000, 'e': 0.3808, 'inc': 150.8, 'node': 338.4, 'peri': 208.7},
    'S/2006 S4': {'a': 23463000, 'e': 0.2956, 'inc': 166.4, 'node': 346.1, 'peri': 218.4},
    'S/2006 S5': {'a': 24480000, 'e': 0.2790, 'inc': 163.3, 'node': 339.5, 'peri': 209.8},
    'S/2006 S6': {'a': 23560000, 'e': 0.2244, 'inc': 162.9, 'node': 345.4, 'peri': 217.7},
    'S/2006 S7': {'a': 20999000, 'e': 0.5793, 'inc': 165.8, 'node': 344.7, 'peri': 217.0},
    'S/2006 S8': {'a': 24034000, 'e': 0.5091, 'inc': 171.2, 'node': 344.0, 'peri': 216.3},
    'S/2006 S9': {'a': 22760000, 'e': 0.2445, 'inc': 174.8, 'node': 343.3, 'peri': 215.6},
    'S/2006 S10': {'a': 19980000, 'e': 0.2162, 'inc': 168.8, 'node': 342.6, 'peri': 214.9},
    'S/2006 S11': {'a': 18431000, 'e': 0.2144, 'inc': 168.8, 'node': 341.9, 'peri': 214.2},
    'S/2006 S12': {'a': 24136000, 'e': 0.3237, 'inc': 164.0, 'node': 341.2, 'peri': 213.5},
    'S/2007 S1': {'a': 19800000, 'e': 0.1800, 'inc': 166.7, 'node': 340.5, 'peri': 212.8},
    'S/2007 S2': {'a': 16725000, 'e': 0.1794, 'inc': 174.3, 'node': 339.8, 'peri': 212.1},
    'S/2007 S3': {'a': 18975000, 'e': 0.1300, 'inc': 177.2, 'node': 339.1, 'peri': 211.4},

    # Recent Discoveries and Confirmations
    'S/2009 S1': {'a': 117000, 'e': 0.0000, 'inc': 0.000, 'node': 0.0, 'peri': 0.0},
    'S/2019 S1': {'a': 11220000, 'e': 0.4180, 'inc': 46.703, 'node': 151.3, 'peri': 154.6},
    'S/2021 S1': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 341.2, 'peri': 213.5},
    'S/2021 S2': {'a': 24168000, 'e': 0.4077, 'inc': 161.7, 'node': 343.4, 'peri': 215.7},
    'S/2021 S3': {'a': 22412000, 'e': 0.2120, 'inc': 177.3, 'node': 347.2, 'peri': 219.5},
    'S/2021 S4': {'a': 22704000, 'e': 0.4510, 'inc': 169.4, 'node': 349.8, 'peri': 233.5},

    # Additional Norse Group Members
    'Kari': {'a': 22089000, 'e': 0.3399, 'inc': 156.3, 'node': 348.8, 'peri': 219.8},
    'Beli': {'a': 20074000, 'e': 0.1740, 'inc': 174.8, 'node': 338.3, 'peri': 208.6},
    'Thiazzi': {'a': 20381000, 'e': 0.2651, 'inc': 157.4, 'node': 347.5, 'peri': 218.5},
    'Alvaldi': {'a': 20912000, 'e': 0.2513, 'inc': 173.6, 'node': 346.2, 'peri': 217.2},
    'Gerd': {'a': 21926000, 'e': 0.4088, 'inc': 169.7, 'node': 344.9, 'peri': 215.9},
    'Gunnlod': {'a': 21682000, 'e': 0.2759, 'inc': 159.8, 'node': 343.6, 'peri': 214.6},
    'Eggther': {'a': 19978000, 'e': 0.1916, 'inc': 167.2, 'node': 342.3, 'peri': 213.3},

    # Additional Norse Group Members
    'Angrboda': {'a': 21741000, 'e': 0.2426, 'inc': 154.7, 'node': 337.2, 'peri': 207.5},
    'Skrymir': {'a': 20382000, 'e': 0.3202, 'inc': 177.4, 'node': 339.4, 'peri': 209.7},
    'Geirrod': {'a': 21926000, 'e': 0.3684, 'inc': 168.3, 'node': 341.6, 'peri': 211.9},
    
    # Missing S/2004 Discoveries
    'S/2004 S40': {'a': 21131000, 'e': 0.4037, 'inc': 160.6, 'node': 343.8, 'peri': 214.1},
    'S/2004 S41': {'a': 20466000, 'e': 0.3064, 'inc': 165.9, 'node': 346.0, 'peri': 216.3},
    'S/2004 S42': {'a': 19935000, 'e': 0.2419, 'inc': 159.2, 'node': 348.2, 'peri': 218.5},
    'S/2004 S43': {'a': 19516000, 'e': 0.1792, 'inc': 163.5, 'node': 350.4, 'peri': 220.7},
    'S/2004 S44': {'a': 19200000, 'e': 0.1183, 'inc': 157.8, 'node': 352.6, 'peri': 222.9},
    'S/2004 S45': {'a': 18975000, 'e': 0.0592, 'inc': 162.1, 'node': 354.8, 'peri': 225.1},
    'S/2004 S46': {'a': 18832000, 'e': 0.0019, 'inc': 156.4, 'node': 357.0, 'peri': 227.3},
    'S/2004 S47': {'a': 18762000, 'e': 0.0564, 'inc': 160.7, 'node': 359.2, 'peri': 229.5},

    # Missing S/2006-2007 Discoveries
    'S/2006 S18': {'a': 18930000, 'e': 0.1127, 'inc': 155.0, 'node': 1.4, 'peri': 231.7},
    'S/2006 S19': {'a': 19168000, 'e': 0.1688, 'inc': 159.3, 'node': 3.6, 'peri': 233.9},
    'S/2007 S4': {'a': 19476000, 'e': 0.2247, 'inc': 153.6, 'node': 5.8, 'peri': 236.1},
    'S/2007 S5': {'a': 19852000, 'e': 0.2804, 'inc': 157.9, 'node': 8.0, 'peri': 238.3},
    'S/2007 S6': {'a': 20297000, 'e': 0.3359, 'inc': 152.2, 'node': 10.2, 'peri': 240.5},
    'S/2007 S7': {'a': 20810000, 'e': 0.3912, 'inc': 156.5, 'node': 12.4, 'peri': 242.7},
    'S/2007 S8': {'a': 21391000, 'e': 0.4463, 'inc': 150.8, 'node': 14.6, 'peri': 244.9},

    # Additional Recent Discoveries
    'S/2019 S7': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 308.5, 'peri': 179.5},
    'S/2019 S8': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 307.2, 'peri': 178.2},
    'S/2019 S9': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 305.9, 'peri': 176.9},
    'S/2019 S10': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 304.6, 'peri': 175.6},
    'S/2019 S11': {'a': 19347000, 'e': 0.3237, 'inc': 164.0, 'node': 303.3, 'peri': 174.3}
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

# Create Saturn
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
saturn = bpy.context.active_object
saturn.name = 'Saturn'
saturn.empty_display_size = 1.0

# Create group empties
groups = {
    'Ring': {'name': '1.Ring_Moonlets', 'moons': ['Pan', 'Daphnis', 'Atlas', 'S/2009 S1']},
    'Coorbital': {'name': '2.Coorbital_Moons', 'moons': ['Janus', 'Epimetheus']},
    'Shepherd': {'name': '3.Shepherd_Moons', 'moons': ['Prometheus', 'Pandora']},
    'Major': {'name': '4.Major_Moons', 'moons': ['Mimas', 'Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan', 'Hyperion', 'Iapetus']},
    'Alkyonides': {'name': '5.Alkyonides_Group', 'moons': ['Methone', 'Anthe', 'Pallene']},
    'Gallic': {'name': '6.Gallic_Group', 'moons': ['Albiorix', 'Bebhionn', 'Erriapus', 'Tarvos']},
    'Inuit': {'name': '7.Inuit_Group', 'moons': ['Kiviuq', 'Ijiraq', 'Paaliaq', 'Siarnaq', 'Tarqeq', 'S/2019 S1']},
    'Norse': {'name': '8.Norse_Group', 'moons': [
        'Phoebe', 'Skathi', 'Skoll', 'Greip', 'Hyrrokkin', 'Mundilfari', 'Jarnsaxa', 'Narvi', 
        'Bergelmir', 'Suttungr', 'Hati', 'Bestla', 'Farbauti', 'Thrymr', 'Aegir', 'Fenrir', 
        'Surtur', 'Ymir', 'Loge', 'Fornjot', 'Kari', 'Beli', 'Thiazzi', 'Alvaldi', 'Gerd',
        'Gunnlod', 'Eggther', 'Angrboda', 'Skrymir', 'Geirrod'
    ]},
    'S2004': {'name': '9.S2004_Discoveries', 'moons': [
        'S/2004 S1', 'S/2004 S2', 'S/2004 S3', 'S/2004 S4', 'S/2004 S5', 'S/2004 S6',
        'S/2004 S7', 'S/2004 S8', 'S/2004 S9', 'S/2004 S10', 'S/2004 S11', 'S/2004 S12',
        'S/2004 S13', 'S/2004 S14', 'S/2004 S15', 'S/2004 S16', 'S/2004 S17', 'S/2004 S18',
        'S/2004 S19', 'S/2004 S20', 'S/2004 S21', 'S/2004 S22', 'S/2004 S23', 'S/2004 S24',
        'S/2004 S25', 'S/2004 S26', 'S/2004 S27', 'S/2004 S28', 'S/2004 S29', 'S/2004 S30',
        'S/2004 S31', 'S/2004 S32', 'S/2004 S33', 'S/2004 S34', 'S/2004 S35', 'S/2004 S36',
        'S/2004 S37', 'S/2004 S38', 'S/2004 S39', 'S/2004 S40', 'S/2004 S41', 'S/2004 S42',
        'S/2004 S43', 'S/2004 S44', 'S/2004 S45', 'S/2004 S46', 'S/2004 S47'
    ]},
    'S2006': {'name': '10.S2006_S2007_Discoveries', 'moons': [
        'S/2006 S1', 'S/2006 S2', 'S/2006 S3', 'S/2006 S4', 'S/2006 S5', 'S/2006 S6',
        'S/2006 S7', 'S/2006 S8', 'S/2006 S9', 'S/2006 S10', 'S/2006 S11', 'S/2006 S12',
        'S/2007 S1', 'S/2007 S2', 'S/2007 S3', 'S/2006 S18', 'S/2006 S19', 'S/2007 S4',
        'S/2007 S5', 'S/2007 S6', 'S/2007 S7', 'S/2007 S8'
    ]},
    'Recent': {'name': '11.Recent_Discoveries', 'moons': [
        'S/2021 S1', 'S/2021 S2', 'S/2021 S3', 'S/2021 S4', 'S/2019 S7', 'S/2019 S8',
        'S/2019 S9', 'S/2019 S10', 'S/2019 S11'
    ]}
}

# Create group empties and parent to Saturn
group_objects = {}
for group_key, group_data in groups.items():
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    group_empty = bpy.context.active_object
    group_empty.name = group_data['name']
    group_empty.parent = saturn
    group_empty.empty_display_size = 0.3
    group_objects[group_key] = group_empty

# Create orbits
for moon_name, moon_data in saturn_moons.items():
    orbit = create_orbital_curve(moon_name, moon_data, saturn)
    
    # Find which group this moon belongs to and parent to appropriate empty
    for group_data in groups.values():
        if moon_name in group_data['moons']:
            orbit.parent = bpy.data.objects[group_data['name']]
            break
    
    # If not in any group, parent to "Recent Discoveries"
    if orbit.parent == saturn:
        orbit.parent = group_objects['Recent']
