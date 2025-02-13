import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from skyfield.api import load, utc
from datetime import datetime, timedelta

# Set up the plot style
plt.style.use('dark_background')

# Create figure and axes
fig = plt.figure(figsize=(20, 20))
ax = fig.add_axes([0.1, 0.1, 0.6, 0.8])
ax_inset = fig.add_axes([0.65, 0.1, 0.2, 0.2])

# Load the planetary ephemeris
planets = load('de440.bsp')

# Set up time range
ts = load.timescale()
t0 = datetime(2350, 1, 1)
# Use 30-day steps instead of 365-day steps (about monthly resolution)
times = [t0 + timedelta(days=i*30) for i in range(171*12)]  # 170 years with monthly steps
times_ts = ts.from_datetimes([t.replace(tzinfo=utc) for t in times])

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

# Pre-calculate all positions to speed up animation
planet_positions = []
for t in times_ts:
    positions = []
    for name, planet, color in planet_data:
        pos = (planet - sun).at(t)
        x, y, _ = pos.position.au
        positions.append((x, y))
    planet_positions.append(positions)

def init():
    ax.clear()
    ax_inset.clear()
    
    # Set up main plot
    ax.set_facecolor('#000510')
    ax.grid(True, alpha=0.1)
    ax.set_aspect('equal')
    
    # Set up inset plot
    ax_inset.set_facecolor('#000510')
    ax_inset.grid(True, alpha=0.1)
    ax_inset.set_aspect('equal')
    
    return []

def animate(frame):
    # Clear previous frame
    ax.clear()
    ax_inset.clear()
    
    # Set up plots
    ax.set_facecolor('#000510')
    ax.grid(True, alpha=0.1)
    ax.set_aspect('equal')
    ax_inset.set_facecolor('#000510')
    ax_inset.grid(True, alpha=0.1)
    ax_inset.set_aspect('equal')
    
    # Plot current positions
    for i, (name, _, color) in enumerate(planet_data):
        x, y = planet_positions[frame][i]
        
        # Main plot
        ax.scatter(x, y, c=color, s=25, label=name, zorder=3)
        ax.annotate(name, (x, y), xytext=(5, 5), 
                   textcoords='offset points', color=color, fontsize=8)
        
        # Plot orbit trail - much longer trail now
        trail_length = 600  # 600 months = 50 years of trail
        start_frame = max(0, frame - trail_length)
        trail_x = [planet_positions[f][i][0] for f in range(start_frame, frame+1)]
        trail_y = [planet_positions[f][i][1] for f in range(start_frame, frame+1)]
        
        # Main plot trails
        ax.plot(trail_x, trail_y, color=color, alpha=0.3, linewidth=1)
        
        # Plot trails in inset for inner planets
        if i < 4:  # Inner planets
            # Draw longer trails in inset view for better visibility
            inset_trail_x = trail_x
            inset_trail_y = trail_y
            ax_inset.plot(inset_trail_x, inset_trail_y, color=color, alpha=0.3, linewidth=1)

        
        # Inset plot (inner planets only)
        if i < 4:
            ax_inset.scatter(x, y, c=color, s=25, zorder=3)
            ax_inset.annotate(name, (x, y), xytext=(3, 3),
                          textcoords='offset points', color=color, fontsize=6)
    
    # Plot Sun
    ax.scatter([0], [0], c='yellow', s=100, label='Sun', zorder=2)
    ax_inset.scatter([0], [0], c='yellow', s=50, zorder=2)
    
    # Set limits and labels
    ax.set_xlim(-32, 32)
    ax.set_ylim(-32, 32)
    ax_inset.set_xlim(-2, 2)
    ax_inset.set_ylim(-2, 2)
    
    # Update title with current date
    current_date = times[frame]
    ax.set_title(f'Solar System Planet Positions\n{current_date.strftime("%B %d, %Y")}', 
                 color='white', pad=20)
    ax_inset.set_title('Inner Solar System', color='white', fontsize=8, pad=5)
    
    ax.set_xlabel('Distance (AU)', color='white')
    ax.set_ylabel('Distance (AU)', color='white')
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    
    return []

# Create animation
anim = animation.FuncAnimation(fig, animate, init_func=init,
                             frames=len(times), interval=100,  # Slower animation
                             blit=True)

# Save animation (uncomment to save)
# anim.save('solar_system_2350_2520.mp4', writer='ffmpeg', fps=30)

plt.show()