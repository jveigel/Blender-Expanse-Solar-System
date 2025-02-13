import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, utc
from datetime import datetime

# Set up the plot style
plt.style.use('dark_background')
# Create figure with specific size and layout
fig = plt.figure(figsize=(38.40, 21.60), dpi=100)
# Create main axes with proper spacing for legend
ax = fig.add_axes((0.1, 0.1, 0.6, 0.8))

# Load the planetary ephemeris
planets = load('de440.bsp')

# Set up our time
ts = load.timescale()
# Set up our time for planet positions
# Define reference date and time span
REFERENCE_DATE = datetime(2025, 1, 1, tzinfo=utc)
TIME_SPAN_YEARS = 170

t = ts.from_datetime(REFERENCE_DATE)  # This is our reference time for planet positions

# Get the sun and planets
sun = planets['sun']
planet_data = [
    ('Mercury', planets['mercury barycenter'], '#A0522D'),
    ('Venus', planets['venus barycenter'], '#DEB887'),
    ('Earth', planets['earth barycenter'], '#4169E1'),
    ('Mars', planets['mars barycenter'], '#CD5C5C'),
    ('Jupiter', planets['jupiter barycenter'], '#DAA520'),
    ('Saturn', planets['saturn barycenter'], '#F4A460'),
    ('Uranus', planets['uranus barycenter'], '#87CEEB'),
    ('Neptune', planets['neptune barycenter'], '#4682B4')
]

# Calculate and plot actual orbital paths
# Create time range covering TIME_SPAN_YEARS to ensure complete orbits for all planets
t0 = ts.from_datetime(REFERENCE_DATE)  # Start from reference date
t1 = ts.from_datetime(REFERENCE_DATE.replace(year=REFERENCE_DATE.year + TIME_SPAN_YEARS))  # Add TIME_SPAN_YEARS
times = ts.linspace(t0, t1, 5000)  # More points for smoother orbits

for name, planet, color in planet_data:
    # Calculate orbital path
    positions = (planet - sun).at(times)
    x, y, _ = positions.position.au
    
    # Plot orbit
    ax.plot(x, y, '--', color='#545454', alpha=0.5, zorder=1)
    
    # Calculate and plot current planet position
    pos = (planet - sun).at(t)
    current_x, current_y, _ = pos.position.au
    ax.scatter(current_x, current_y, c=color, s=25, label=name, zorder=3)
    
    # Add planet label
    ax.annotate(name, (current_x, current_y), xytext=(5, 5), 
                textcoords='offset points', color=color, fontsize=8)

# Plot the Sun
ax.scatter([0], [0], c='yellow', s=100, label='Sun', zorder=2)

# Customize the plot
ax.set_aspect('equal')
ax.grid(True, alpha=0.1)
ax.set_facecolor('#000510')
fig.set_facecolor('#000510')

# Set title and labels
ax.set_title(f'Solar System Planet Positions\n{REFERENCE_DATE.strftime("%B %d, %Y")}', 
             color='white', pad=20)
ax.set_xlabel('Distance (AU)', color='white')
ax.set_ylabel('Distance (AU)', color='white')

# Add legend with proper spacing
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

# Set axis limits to show all planets
max_dist = 32  # Just beyond Neptune's orbit
ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)

# Create inset plot for inner planets
ax_inset = fig.add_axes((0.65, 0.1, 0.5, 0.5))
max_dist_inner = 2  # Just beyond Mars' orbit

# Plot inner planets in inset
for name, planet, color in planet_data[:4]:  # Inner planets only
    # Calculate orbital path
    positions = (planet - sun).at(times)
    x, y, _ = positions.position.au

    # Plot orbit
    ax_inset.plot(x, y, '--', color='#545454', alpha=0.5)
    
    # Plot current position
    pos = (planet - sun).at(t)
    current_x, current_y, _ = pos.position.au
    ax_inset.scatter(current_x, current_y, c=color, s=25)
    
    # Add label
    ax_inset.annotate(name, (current_x, current_y), xytext=(3, 3),
                      textcoords='offset points', color=color, fontsize=6)

# Plot Sun in inset
ax_inset.scatter([0], [0], c='yellow', s=50)

# Customize inset plot
ax_inset.set_aspect('equal')
ax_inset.grid(True, alpha=0.1)
ax_inset.set_facecolor('#000510')
ax_inset.set_title('Inner Solar System', color='white', fontsize=8, pad=5)
ax_inset.set_xlim(-max_dist_inner, max_dist_inner)
ax_inset.set_ylim(-max_dist_inner, max_dist_inner)

# Replace plt.show() with savefig
plt.savefig(f'Solar_System_{REFERENCE_DATE.strftime("%Y_%m_%d")}.png', 
            dpi=100, bbox_inches='tight', facecolor='#000510')
plt.close()