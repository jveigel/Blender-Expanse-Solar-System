"""
Relativistic Brachistochrone Calculator - Revised
Incorporates variable mass effects and numerical integration
"""
import math
import csv
from datetime import timedelta, datetime
import os
import numpy as np

# Physical Constants
C = 299792458  # Speed of light in m/s
LY_TO_M = 9.461e15  # Light years to meters
G = 9.80665  # Standard gravity in m/s²

# Power and Engine Parameters
TOTAL_POWER = 100e12  # Total spacecraft power (100 TW)
EXHAUST_V = 0.068 * C  # 5% of light speed
NUM_ENGINES = 4

def calculate_engine_parameters(total_power, exhaust_v, num_engines):
    """Calculate engine parameters based on power constraints"""
    power_per_engine = total_power / num_engines
    mass_flow_per_engine = (2 * power_per_engine) / (exhaust_v**2)
    thrust_per_engine = mass_flow_per_engine * exhaust_v
    
    return {
        'power_per_engine': power_per_engine,
        'mass_flow_per_engine': mass_flow_per_engine,
        'thrust_per_engine': thrust_per_engine,
        'total_thrust': thrust_per_engine * num_engines,
        'total_mass_flow': mass_flow_per_engine * num_engines
    }

ENGINE_PARAMS = calculate_engine_parameters(TOTAL_POWER, EXHAUST_V, NUM_ENGINES)

# Ship configurations with dry mass and fuel mass
SHIP_CONFIGS = {
    'Ultra Light': {'dry_mass': 1000, 'fuel_mass': 10000},     # 1,000 tons dry, 10,000 tons fuel
    'Light': {'dry_mass': 10000, 'fuel_mass': 100000},         # 10,000 tons dry, 100,000 tons fuel
    'Medium': {'dry_mass': 100000, 'fuel_mass': 1000000},      # 100,000 tons dry, 1,000,000 tons fuel
    'Heavy': {'dry_mass': 1000000, 'fuel_mass': 10000000}      # 1,000,000 tons dry, 10,000,000 tons fuel
}

# Mission Parameters
DESTINATIONS = {
    'Alpha Centauri': 4.37,
    'Tau Ceti': 11.9,
    'Barnards Star': 5.96
}

def format_duration(seconds):
    """Convert seconds to years, months, days format"""
    days = seconds / (24 * 3600)
    years = days / 365.25
    remaining_days = days % 365.25
    months = remaining_days / 30.44
    days = remaining_days % 30.44
    return f"{int(years)}y {int(months)}m {int(days)}d"

def calculate_lorentz_factor(velocity):
    """Calculate Lorentz factor (gamma)"""
    beta = velocity / C
    return 1 / math.sqrt(1 - beta**2)

def simulate_burn_phase(initial_mass, thrust, mass_flow, fuel_mass, dt=1):
    """Vectorized burn phase simulation using NumPy"""
    # Pre-calculate number of steps
    n_steps = min(int(fuel_mass / mass_flow / dt), 1000000)
    
    # Create time array
    time = np.arange(n_steps) * dt
    
    # Calculate mass array
    mass = initial_mass - mass_flow * time
    mass = mass[mass > (initial_mass - fuel_mass)]
    n_steps = len(mass)
    time = time[:n_steps]
    
    # Calculate acceleration and gamma arrays
    accel = thrust / mass
    velocity = np.zeros(n_steps)
    
    # Vectorized velocity calculation
    rapidity = np.cumsum(accel * dt / C)
    velocity = C * np.tanh(rapidity)
    
    # Calculate gamma factors
    gamma = 1 / np.sqrt(1 - (velocity/C)**2)
    
    # Calculate distance and coordinate time
    avg_velocity = (velocity[1:] + velocity[:-1]) / 2
    avg_gamma = (gamma[1:] + gamma[:-1]) / 2
    distance = np.sum(avg_velocity * avg_gamma * dt)
    coordinate_time = np.sum(avg_gamma * dt)
    
    return time[-1], coordinate_time, velocity[-1], distance

def calculate_mission_parameters(config):
    """Calculate mission parameters with specified dry and fuel mass"""
    dry_mass_kg = config['dry_mass'] * 1000  # Convert tons to kg
    fuel_mass_kg = config['fuel_mass'] * 1000  # Convert tons to kg
    initial_mass_kg = dry_mass_kg + fuel_mass_kg
    
    params = {'feasible': False}
    
    # Simulate acceleration phase with half the fuel
    accel_time, t_accel, v_accel, s_accel = simulate_burn_phase(
        initial_mass_kg,
        ENGINE_PARAMS['total_thrust'],
        ENGINE_PARAMS['total_mass_flow'],
        fuel_mass_kg/2
    )
    
    # Calculate mass after acceleration
    mass_after_accel = initial_mass_kg - fuel_mass_kg/2
    
    # Simulate deceleration phase with remaining fuel
    decel_time, t_decel, v_decel, s_decel = simulate_burn_phase(
        mass_after_accel,
        ENGINE_PARAMS['total_thrust'],
        ENGINE_PARAMS['total_mass_flow'],
        fuel_mass_kg/2
    )
    
    params.update({
        'ship_time': accel_time + decel_time,
        'earth_time': t_accel + t_decel,
        'max_velocity': v_accel,
        'proper_acceleration': ENGINE_PARAMS['total_thrust'] / initial_mass_kg,
        'total_distance': s_accel + s_decel,
        'feasible': True,
        'gamma_max': calculate_lorentz_factor(v_accel),
        'mass_ratio': initial_mass_kg / dry_mass_kg
    })
    
    return params

def generate_results():
    """Generate results for all ship configurations and destinations"""
    results = []
    total_calcs = len(SHIP_CONFIGS) * len(DESTINATIONS)
    current_calc = 0
    
    print("\nCalculating trajectories...")
    for config_name, config in SHIP_CONFIGS.items():
        params = calculate_mission_parameters(config)
        max_range_ly = params['total_distance'] / LY_TO_M
        
        for dest, dist in DESTINATIONS.items():
            current_calc += 1
            print(f"Processing {config_name} to {dest} ({current_calc}/{total_calcs})")
            
            if dist > max_range_ly:
                print(f"  Not feasible - insufficient range")
                continue
            
            # Calculate coast phase if needed
            coast_distance = dist * LY_TO_M - params['total_distance']
            if coast_distance > 0:
                coast_velocity = params['max_velocity']
                gamma = calculate_lorentz_factor(coast_velocity)
                coast_time = coast_distance / (coast_velocity * gamma)
                total_ship_time = params['ship_time'] + coast_time/gamma
                total_earth_time = params['earth_time'] + coast_time
            else:
                total_ship_time = params['ship_time']
                total_earth_time = params['earth_time']
            
            results.append({
                'Config': config_name,
                'Dry Mass (tons)': f"{config['dry_mass']:,}",
                'Fuel Mass (tons)': f"{config['fuel_mass']:,}",
                'Mass Ratio': f"{params['mass_ratio']:.1f}",
                'Destination': dest,
                'Distance (ly)': dist,
                'Proper Acceleration (g)': f"{(params['proper_acceleration']/G):.3f}",
                'Ship Time': format_duration(total_ship_time),
                'Earth Time': format_duration(total_earth_time),
                'Time Dilation Factor': f"{params['gamma_max']:.1f}",
                'Max Velocity (%c)': f"{(params['max_velocity']/C*100):.1f}"
            })
            print(f"  Complete - Ship time: {format_duration(total_ship_time)}")
    
    return results

def save_to_csv(data, base_filename='relativistic_brachistochrone'):
    """Save results to CSV file with timestamp in exports folder"""
    if not data:
        print("\nNo feasible missions found - no results to save")
        return
        
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'exports/{base_filename}_{timestamp}.csv'
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\nResults saved to {filename}")

def print_summary(results):
    """Print formatted summary of results"""
    print("\nD-He3 Fusion Drive Relativistic Brachistochrone Calculator")
    print("=======================================================")
    print(f"\nPower and Engine Configuration:")
    print(f"Total Power: {TOTAL_POWER/1e12:.1f} TW")
    print(f"Number of Engines: {NUM_ENGINES}")
    print(f"Power per Engine: {ENGINE_PARAMS['power_per_engine']/1e12:.1f} TW")
    print(f"Total Thrust: {ENGINE_PARAMS['total_thrust']/1e6:.1f} MN")
    print(f"Exhaust Velocity: {EXHAUST_V/C*100:.1f}% c")
    print(f"Mass Flow Rate: {ENGINE_PARAMS['total_mass_flow']:.1f} kg/s")
    
    if not results:
        print("\nNo feasible missions found with current parameters")
        return

    print("\nMission Results (Feasible Missions Only):")
    current_config = ""
    for r in results:
        if r['Config'] != current_config:
            current_config = r['Config']
            print(f"\n{current_config} Configuration:")
            print(f"Dry Mass: {r['Dry Mass (tons)']} tons")
            print(f"Fuel Mass: {r['Fuel Mass (tons)']} tons")
            print("-" * 120)
            print(f"{'Destination':<15} | {'Accel (g)':<10} | {'Mass Ratio':<10} | {'Ship Time':<15} | "
                  f"{'Earth Time':<15} | {'γ factor':<8} | {'Max Speed':<10}")
            print("-" * 120)
        
        print(f"{r['Destination']:<15} | {r['Proper Acceleration (g)']:<10} | "
              f"{r['Mass Ratio']:<10} | {r['Ship Time']:<15} | {r['Earth Time']:<15} | "
              f"{r['Time Dilation Factor']:<8} | {r['Max Velocity (%c)']:>5}% c")

if __name__ == "__main__":
    results = generate_results()
    save_to_csv(results)
    print_summary(results)