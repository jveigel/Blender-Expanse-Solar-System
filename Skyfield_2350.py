import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, utc
from datetime import datetime

# Set up the plot style
plt.style.use('dark_background')

# Create figure with specific size and layout
fig = plt.figure(figsize=(38.40, 21.60), dpi=100)
ax = fig.add_axes((0.1, 0.1, 0.6, 0.8))

# Load the planetary ephemeris
planets = load('de440.bsp')

# Get the sun and planets with approximate orbital periods (years)
sun = planets['sun']
planet_data = [
    ('Mercury', planets['mercury barycenter'], '#A0522D', 0.24),
    ('Venus', planets['venus barycenter'], '#DEB887', 0.62),
    ('Earth', planets['earth barycenter'], '#4169E1', 1.0),
    ('Mars', planets['mars barycenter'], '#CD5C5C', 1.88),
    ('Jupiter', planets['jupiter barycenter'], '#DAA520', 11.86),
    ('Saturn', planets['saturn barycenter'], '#F4A460', 29.46),
    ('Uranus', planets['uranus barycenter'], '#87CEEB', 84.01),
    ('Neptune', planets['neptune barycenter'], '#4682B4', 164.79)
]

# Set up time
ts = load.timescale()
REFERENCE_DATE = datetime(2350, 1, 1, tzinfo=utc)
t = ts.from_datetime(REFERENCE_DATE)

# For each planet, calculate and plot its orbital path
for name, planet, color, period in planet_data:
    # Calculate number of points based on orbital period
    # More points for longer periods to maintain point density
    n_points = int(20000 * np.sqrt(period))  # Square root to balance sampling
    
    # Use fixed 2-year time span for all planets
    t0 = ts.from_datetime(REFERENCE_DATE)
    t1 = ts.from_datetime(REFERENCE_DATE.replace(year=REFERENCE_DATE.year + 2))
    times = ts.linspace(t0, t1, n_points)
    
    # Calculate orbital path
    positions = (planet - sun).at(times)
    x = positions.position.au[0]
    y = positions.position.au[1]
    
    # Plot orbit
    ax.plot(x, y, '--', color='#545454', alpha=1, zorder=1, linewidth=1)
    
    # Calculate and plot current planet position
    pos = (planet - sun).at(t)
    current_x = pos.position.au[0]
    current_y = pos.position.au[1]
    ax.scatter(current_x, current_y, c=color, s=25, label=name, zorder=3)
    
    # Add planet label
    ax.annotate(name, (current_x, current_y), xytext=(5, 5), 
                textcoords='offset points', color=color, fontsize=8)

# Plot the Sun
ax.scatter([0], [0], c='yellow', s=100, label='Sun', zorder=2)

# Create inset plot for inner planets
ax_inset = fig.add_axes((0.65, 0.1, 0.5, 0.5))
max_dist_inner = 2

# Plot inner planets in inset
for name, planet, color, period in planet_data[:4]:
    # Calculate orbital path with high sampling for inner planets
    n_points = int(50000 * np.sqrt(period))  # Even more points for inner planets
    t0 = ts.from_datetime(REFERENCE_DATE)
    t1 = ts.from_datetime(REFERENCE_DATE.replace(year=REFERENCE_DATE.year + 2))
    times = ts.linspace(t0, t1, n_points)
    
    positions = (planet - sun).at(times)
    x = positions.position.au[0]
    y = positions.position.au[1]

    # Plot orbit
    ax_inset.plot(x, y, '--', color='#545454', alpha=1, linewidth=1)
    
    # Plot current position
    pos = (planet - sun).at(t)
    current_x = pos.position.au[0]
    current_y = pos.position.au[1]
    ax_inset.scatter(current_x, current_y, c=color, s=25)
    
    # Add label
    ax_inset.annotate(name, (current_x, current_y), xytext=(3, 3),
                      textcoords='offset points', color=color, fontsize=6)

# Plot Sun in inset
ax_inset.scatter([0], [0], c='yellow', s=50)

# Customize both plots
for axis in [ax, ax_inset]:
    axis.set_aspect('equal')
    axis.grid(True, alpha=0.1)
    axis.set_facecolor('#000510')
    
# Set axis limits for main plot
max_dist = 32
ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)

# Set axis limits for inset
ax_inset.set_xlim(-max_dist_inner, max_dist_inner)
ax_inset.set_ylim(-max_dist_inner, max_dist_inner)

# Set titles and labels
ax.set_title(f'Solar System Planet Positions (Orthographic Projection)\n{REFERENCE_DATE.strftime("%B %d, %Y")}', 
             color='white', pad=20)
ax_inset.set_title('Inner Solar System', color='white', fontsize=8, pad=5)

# Add legend
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

# Set figure background
fig.set_facecolor('#000510')

# Save the figure
plt.savefig(f'Solar_System_Orthographic_{REFERENCE_DATE.strftime("%Y_%m_%d")}.png', 
            dpi=100, bbox_inches='tight', facecolor='#000510')
plt.close()