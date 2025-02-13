import numpy as np
import matplotlib.pyplot as plt

class SolarSystem:
    def __init__(self):
        # Orbital data: J2000 epoch values (NASA DE440/DE441)
        self.planets = {
            'Mercury': {'a': 0.387098, 'e': 0.205630, 'inc': 7.005, 'node': 48.331, 'peri': 29.124, 'color': '#A0522D'},
            'Venus': {'a': 0.723332, 'e': 0.006772, 'inc': 3.394, 'node': 76.680, 'peri': 54.884, 'color': '#DEB887'},
            'Earth': {'a': 1.000000, 'e': 0.016708, 'inc': 0.000, 'node': 0.000, 'peri': 102.937, 'color': '#4169E1'},
            'Mars': {'a': 1.523679, 'e': 0.093401, 'inc': 1.850, 'node': 49.558, 'peri': 286.502, 'color': '#CD5C5C'},
            'Ceres': {'a': 2.765348, 'e': 0.075823, 'inc': 10.593, 'node': 80.393, 'peri': 73.597, 'color': '#808080'},
            'Eros': {'a': 1.458432, 'e': 0.222974, 'inc': 10.829, 'node': 304.435, 'peri': 178.641, 'color': '#8B4513'},
            'Jupiter': {'a': 5.202561, 'e': 0.048498, 'inc': 1.303, 'node': 100.556, 'peri': 275.066, 'color': '#DAA520'},
            'Saturn': {'a': 9.537070, 'e': 0.054309, 'inc': 2.485, 'node': 113.715, 'peri': 338.716, 'color': '#F4A460'},
            'Uranus': {'a': 19.191264, 'e': 0.047318, 'inc': 0.773, 'node': 74.006, 'peri': 96.998, 'color': '#87CEEB'},
            'Neptune': {'a': 30.068963, 'e': 0.008676, 'inc': 1.770, 'node': 131.783, 'peri': 273.187, 'color': '#1E90FF'}
        }

    def plot_top_view(self):
        plt.figure(figsize=(32, 32))
        ax = plt.gca()
        ax.set_facecolor('none')
        
        plt.plot(0, 0, 'yo', markersize=.1, label='Sun')

        theta = np.linspace(0, 2*np.pi, 10000)
        
        for planet, data in self.planets.items():
            # Get orbital parameters
            a = data['a']
            e = data['e']
            inc = np.radians(data['inc'])
            node = np.radians(data['node'])
            peri = np.radians(data['peri'])
            
            # Calculate orbital path using polar form of ellipse
            r = a * (1 - e**2) / (1 + e * np.cos(theta))
            
            # Initial position in orbital plane
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = np.zeros_like(x)
            
            # 1. Rotate by argument of perihelion (ω) around z-axis
            x_peri = x * np.cos(peri) - y * np.sin(peri)
            y_peri = x * np.sin(peri) + y * np.cos(peri)
            z_peri = z
            
            # 2. Rotate by inclination (i) around x-axis
            y_inc = y_peri * np.cos(inc) - z_peri * np.sin(inc)
            z_inc = y_peri * np.sin(inc) + z_peri * np.cos(inc)
            
            # 3. Rotate by longitude of node (Ω) around z-axis
            x_final = x_peri * np.cos(node) - y_inc * np.sin(node)
            y_final = x_peri * np.sin(node) + y_inc * np.cos(node)
            
            # Plot orbit
            markersize = 0.75 if planet in ['Ceres', 'Eros'] else 1.5
            linestyle = '--' if planet in ['Ceres', 'Eros'] else '-'
            plt.plot(x_final, y_final, linestyle, color=data['color'], alpha=1, 
                    label=f"{planet} (e={data['e']:.3f})", linewidth=0.15)
            
            # Plot planet at a random position
            random_pos = np.random.randint(0, len(theta))
            plt.plot(x_final[random_pos], y_final[random_pos], 'o', 
                    color=data['color'], markersize=markersize)

            # Calculate and plot ascending node
            asc_node_theta = -peri  # True anomaly at ascending node
            r_an = a * (1 - e**2) / (1 + e * np.cos(asc_node_theta))
            x_an = r_an * np.cos(asc_node_theta)
            y_an = r_an * np.sin(asc_node_theta)
            
            # Transform ascending node through same rotations
            x_an_rot = x_an * np.cos(peri) - y_an * np.sin(peri)
            y_an_rot = x_an * np.sin(peri) + y_an * np.cos(peri)
            y_an_inc = y_an_rot * np.cos(inc)
            x_an_final = x_an_rot * np.cos(node) - y_an_inc * np.sin(node)
            y_an_final = x_an_rot * np.sin(node) + y_an_inc * np.cos(node)
            
            plt.plot(x_an_final, y_an_final, '+', color=data['color'], 
                    markersize=2, alpha=0.5)

        # Customize plot
        plt.grid(True, alpha=0.1, color='gray')
        plt.axis('equal')
        plt.title('Scale-Accurate Solar System Orbits (J2000 Epoch)\n(with Eccentricity and Orbital Alignment)', 
                 color='gray', size=24)
        plt.xlabel('Distance (AU)', color='gray', size=20)
        plt.ylabel('Distance (AU)', color='gray', size=20)
        
        ax.tick_params(colors='gray', labelsize=16)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), 
                  facecolor='none', edgecolor='gray', labelcolor='gray',
                  fontsize=16)

        plt.savefig('.\exports\solar_system_accurate_top_8k.png', 
                   dpi=300,
                   bbox_inches='tight',
                   transparent=True,
                   pad_inches=0.5)

    def plot_side_view(self):
        pass  # Remove or implement this method

if __name__ == "__main__":
    solar_system = SolarSystem()
    solar_system.plot_top_view() 