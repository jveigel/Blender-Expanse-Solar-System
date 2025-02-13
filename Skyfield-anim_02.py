import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from skyfield.api import load, utc
from datetime import datetime, timedelta

# Load timescale
ts = load.timescale()

# Set up the plot style
plt.style.use('dark_background')

# Create figure and single axis
fig = plt.figure(figsize=(38.40, 21.60), dpi=100)
ax = fig.add_subplot(111)

# Load the planetary ephemeris
planets = load('de440.bsp')

# Set up time range with variables
REFERENCE_DATE = datetime(2300, 1, 1, tzinfo=utc)
TIME_SPAN_YEARS = 100

t0 = REFERENCE_DATE
times = [t0 + timedelta(days=i*60) for i in range(TIME_SPAN_YEARS*6)]  # Bi-monthly steps
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
    ax.set_facecolor('#000510')
    fig.set_facecolor('#000510')
    ax.grid(True, alpha=0.1)
    ax.set_aspect('equal')
    # Remove frame border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return []

def animate(frame):
    ax.clear()
    
    # Set up main plot
    ax.set_facecolor('#000510')
    fig.set_facecolor('#000510')
    ax.grid(True, alpha=0.1)
    ax.set_aspect('equal')
    
    # Remove frame border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Create inset plot for inner planets
    ax_inset = fig.add_axes([0.65, 0.1, 0.5, 0.5])
    max_dist_inner = 2  # Just beyond Mars' orbit
    
    # Plot current positions in both main and inset
    for i, (name, _, color) in enumerate(planet_data):
        x, y = planet_positions[frame][i]
        
        # Main plot
        ax.scatter(x, y, c=color, s=25, label=name, zorder=3)
        ax.annotate(name, (x, y), xytext=(5, 5), 
                   textcoords='offset points', color=color, fontsize=8)
        
        # Plot orbit trail in main plot
        trail_length = 300
        start_frame = max(0, frame - trail_length)
        trail_x = [planet_positions[f][i][0] for f in range(start_frame, frame+1)]
        trail_y = [planet_positions[f][i][1] for f in range(start_frame, frame+1)]
        ax.plot(trail_x, trail_y, color=color, alpha=0.3, linewidth=1)
        
        # Plot inner planets in inset
        if i < 4:  # Only inner planets
            ax_inset.scatter(x, y, c=color, s=25)
            ax_inset.annotate(name, (x, y), xytext=(3, 3),
                          textcoords='offset points', color=color, fontsize=6)
            # Add trails to inset
            ax_inset.plot(trail_x, trail_y, color=color, alpha=0.3, linewidth=1)
    
    # Plot Sun in both plots
    ax.scatter([0], [0], c='yellow', s=100, label='Sun', zorder=2)
    ax_inset.scatter([0], [0], c='yellow', s=50)
    
    # Customize inset plot
    ax_inset.set_aspect('equal')
    ax_inset.grid(True, alpha=0.1)
    ax_inset.set_facecolor('#000510')
    ax_inset.set_title('Inner Solar System', color='white', fontsize=8, pad=5)
    ax_inset.set_xlim(-max_dist_inner, max_dist_inner)
    ax_inset.set_ylim(-max_dist_inner, max_dist_inner)
    
    # Set main plot limits and labels
    ax.set_xlim(-32, 32)
    ax.set_ylim(-32, 32)
    
    # Update title with current date
    current_date = times[frame]
    ax.set_title(f'Solar System Planet Positions\n{current_date.strftime("%B %d, %Y")}', 
                 color='white', pad=20)
    
    ax.set_xlabel('Distance (AU)', color='white')
    ax.set_ylabel('Distance (AU)', color='white')
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    
    return []

# Create animation with adjusted settings
anim = animation.FuncAnimation(fig, animate, init_func=init,
                             frames=len(times), interval=50,  # Reduced interval
                             blit=True)

# Save with more efficient settings
anim.save('solar_system_2350_2520.mp4', 
          writer='ffmpeg', 
          fps=30,  # Reduced from 30
          dpi=100,
          savefig_kwargs={'facecolor':'#000510'},
          # Add extra ffmpeg settings for better compression
          extra_args=['-vcodec', 'libx264', 
                     '-pix_fmt', 'yuv420p',
                     '-crf', '23'])  # Compression quality (18-28 is good, lower=better)
plt.close()