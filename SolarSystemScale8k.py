import numpy as np
import matplotlib.pyplot as plt

class SolarSystem:
    def __init__(self):
        # Orbital data: 
        # a (semi-major axis in AU), 
        # e (eccentricity), inc (inclination), 
        # node (Ω, longitude of ascending node,"right ascension of ascending node"), 
        # peri (ω, argument of perihelion)
        self.planets = {
            'Mercury': {'a': 0.387, 'e': 0.206, 'inc': 7.0, 'node': 48.331, 'peri': 29.124, 'color': '#A0522D'},
            'Venus': {'a': 0.723, 'e': 0.007, 'inc': 3.4, 'node': 76.680, 'peri': 54.884, 'color': '#DEB887'},
            'Earth': {'a': 1.000, 'e': 0.017, 'inc': 0.0, 'node': 0.0, 'peri': 102.937, 'color': '#4169E1'},
            'Mars': {'a': 1.524, 'e': 0.093, 'inc': 1.9, 'node': 49.558, 'peri': 286.502, 'color': '#CD5C5C'},
            'Ceres': {'a': 2.766, 'e': 0.076, 'inc': 10.6, 'node': 80.393, 'peri': 73.597, 'color': '#808080'},
            'Eros': {'a': 1.458, 'e': 0.223, 'inc': 10.8, 'node': 304.435, 'peri': 178.641, 'color': '#8B4513'},
            'Jupiter': {'a': 5.203, 'e': 0.048, 'inc': 1.3, 'node': 100.464, 'peri': 273.867, 'color': '#DAA520'},
            'Saturn': {'a': 9.537, 'e': 0.054, 'inc': 2.5, 'node': 113.665, 'peri': 339.392, 'color': '#F4A460'},
            'Uranus': {'a': 19.191, 'e': 0.047, 'inc': 0.8, 'node': 74.006, 'peri': 96.998, 'color': '#87CEEB'},
            'Neptune': {'a': 30.069, 'e': 0.009, 'inc': 1.8, 'node': 131.783, 'peri': 273.187, 'color': '#1E90FF'}
        }

    def plot_top_view(self):
        # Create a new figure with transparent background
        plt.figure(figsize=(32, 32))  # Removed facecolor
        ax = plt.gca()
        ax.set_facecolor('none')  # Transparent background
        
        # Plot the Sun
        plt.plot(0, 0, 'yo', markersize=.1, label='Sun')

        # Massive increase in orbital resolution
        theta = np.linspace(0, 2*np.pi, 10000)
        
        for planet, data in self.planets.items():
            # Get orbital parameters
            a = data['a']  # semi-major axis
            e = data['e']  # eccentricity
            inc = np.radians(data['inc'])  # inclination
            node = np.radians(data['node'])  # longitude of ascending node
            peri = np.radians(data['peri'])  # argument of perihelion
            
            # Calculate orbital path using polar form of ellipse
            r = a * (1 - e**2) / (1 + e * np.cos(theta))
            
            # Calculate coordinates in orbital plane
            x_orbit = r * np.cos(theta)
            y_orbit = r * np.sin(theta)
            
            # Apply rotation matrices for proper 3D orientation
           
            # First rotate by argument of perihelion
            x_peri = x_orbit * np.cos(peri) - y_orbit * np.sin(peri)
            y_peri = x_orbit * np.sin(peri) + y_orbit * np.cos(peri)
            
             # Then rotate by inclination
            y_inc = y_peri * np.cos(inc)
            z_inc = y_peri * np.sin(inc)
            
            # Finally rotate by longitude of ascending node
            x = x_peri * np.cos(node) - y_inc * np.sin(node)
            y = x_peri * np.sin(node) + y_inc * np.cos(node)
           

            markersize = 0.75 if planet in ['Ceres', 'Eros'] else 1.5
            linestyle = '--' if planet in ['Ceres', 'Eros'] else '-'
            
            # Plot orbit
            plt.plot(x, y, linestyle, color=data['color'], alpha=1, 
                    label=f"{planet} (e={data['e']:.3f})", linewidth=0.15)
            
            # Plot planet at a random position in its orbit
            random_pos = np.random.randint(0, len(theta))
            plt.plot(x[random_pos], y[random_pos], 'o', color=data['color'], 
                    markersize=markersize, label=planet)

            # Plot ascending node point
            node_x = a * np.cos(node)
            node_y = a * np.sin(node)
            plt.plot(node_x, node_y, '+', color=data['color'], 
                    markersize=2, alpha=0.5)

        # Customize the plot
        plt.grid(True, alpha=0.1, color='gray')  # Changed grid color for visibility
        plt.axis('equal')
        plt.title('Scale-Accurate Solar System Orbits\n(with Eccentricity and Orbital Alignment)', 
                 color='gray', size=24)
        plt.xlabel('Distance (AU)', color='gray', size=20)
        plt.ylabel('Distance (AU)', color='gray', size=20)
        
        # Customize ticks with gray font
        ax.tick_params(colors='gray', labelsize=16)
        
        # Add legend with transparent background
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), 
                  facecolor='none', edgecolor='gray', labelcolor='gray',
                  fontsize=16)

        # Save plot in high resolution with transparency
        plt.savefig('solar_system_eccentric_aligned_8k.png', 
                   dpi=300,
                   bbox_inches='tight',
                   transparent=True,  # Enable transparency
                   pad_inches=0.5)

    def plot_side_view(self):
        # Create a new figure with transparent background
        plt.figure(figsize=(32, 16))  # Half height for side view
        ax = plt.gca()
        ax.set_facecolor('none')
        
        # Plot the Sun
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
            
            # Calculate coordinates in orbital plane
            x_orbit = r * np.cos(theta)
            y_orbit = r * np.sin(theta)
            
            # Apply rotation matrices for proper 3D orientation
            # First rotate by argument of perihelion
            x_peri = x_orbit * np.cos(peri) - y_orbit * np.sin(peri)
            y_peri = x_orbit * np.sin(peri) + y_orbit * np.cos(peri)
            
            # Then rotate by inclination
            y_inc = y_peri * np.cos(inc)
            z_inc = y_peri * np.sin(inc)
            
            # Finally rotate by longitude of ascending node
            x = x_peri * np.cos(node) - y_inc * np.sin(node)
            z = z_inc  # Use z coordinate for height above/below plane
            
            # Plot orbit
            markersize = 0.75 if planet in ['Ceres', 'Eros'] else 1.5
            linestyle = '--' if planet in ['Ceres', 'Eros'] else '-'
            
            plt.plot(x, z, linestyle, color=data['color'], alpha=1, 
                    label=f"{planet} (i={data['inc']}°)", linewidth=0.05)
            
            # Plot planet at a random position
            random_pos = np.random.randint(0, len(theta))
            plt.plot(x[random_pos], z[random_pos], 'o', color=data['color'], 
                    markersize=markersize)

        # Customize the plot
        plt.grid(True, alpha=0.1, color='gray')
        plt.axis('equal')
        plt.title('Solar System Orbital Inclinations (Side View)', color='gray', size=24)
        plt.xlabel('Distance (AU)', color='gray', size=20)
        plt.ylabel('Height Above/Below Ecliptic (AU)', color='gray', size=20)
        
        # Customize ticks
        ax.tick_params(colors='gray', labelsize=16)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), 
                  facecolor='none', edgecolor='gray', labelcolor='gray',
                  fontsize=16)

        # Add reference line for ecliptic plane
        plt.axhline(y=0, color='gray', alpha=0.2, linestyle=':', linewidth=0.5)

        # Save plot
        plt.savefig('solar_system_inclination_side_8k.png', 
                   dpi=300,
                   bbox_inches='tight',
                   transparent=True,
                   pad_inches=0.5)

if __name__ == "__main__":
    solar_system = SolarSystem()
    solar_system.plot_top_view()  # Top view
    solar_system.plot_side_view()  # Side view
