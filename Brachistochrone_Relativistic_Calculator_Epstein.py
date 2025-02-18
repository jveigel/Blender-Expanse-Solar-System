"""
Relativistic Brachistochrone Calculator for D-He3 Fusion Drive
Implements proper relativistic mechanics for interstellar trajectories
"""
import math
import csv
from datetime import timedelta, datetime
import os

# Physical Constants
C = 299792458  # Speed of light in m/s
LY_TO_M = 9.461e15  # Light years to meters
G = 9.80665  # Standard gravity in m/s²

# Power and Engine Parameters
TOTAL_POWER = 100e12  # Total spacecraft power (100 TW)
EXHAUST_V = 0.05 * C  # 5% of light speed
NUM_ENGINES = 4

def calculate_engine_parameters(total_power, exhaust_v, num_engines):
    """Calculate engine parameters based on power constraints"""
    power_per_engine = total_power / num_engines
    mass_flow_per_engine = (2 * power_per_engine) / (exhaust_v * exhaust_v)
    thrust_per_engine = mass_flow_per_engine * exhaust_v
    
    return {
        'power_per_engine': power_per_engine,
        'mass_flow_per_engine': mass_flow_per_engine,
        'thrust_per_engine': thrust_per_engine,
        'total_thrust': thrust_per_engine * num_engines,
        'total_mass_flow': mass_flow_per_engine * num_engines
    }

ENGINE_PARAMS = calculate_engine_parameters(TOTAL_POWER, EXHAUST_V, NUM_ENGINES)

# Ship configurations
SHIP_CONFIGS = {
    'Ultra Light': 1000,     # 1,000 tons dry mass
    'Light': 10000,         # 10,000 tons dry mass
    'Medium': 100000,       # 100,000 tons dry mass
    'Heavy': 1000000       # 1,000,000 tons dry mass
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
    return 1 / math.sqrt(1 - beta * beta)

def calculate_proper_acceleration(thrust, mass):
    """Calculate proper acceleration (acceleration in ship's frame)"""
    return thrust / mass

def calculate_relativistic_velocity(proper_acceleration, proper_time):
    """Calculate velocity using rapidity"""
    return C * math.tanh(proper_acceleration * proper_time / C)

def calculate_relativistic_deltav(exhaust_v, mass_ratio):
    """Calculate delta-v using relativistic rocket equation"""
    beta = exhaust_v / C
    return C * math.tanh(beta * math.log(mass_ratio))

def calculate_relativistic_brachistochrone(distance_m, proper_acceleration):
    """Calculate relativistic brachistochrone trajectory times and distances"""
    # Using relativistic hyperbolic motion equations
    # For constant proper acceleration
    
    # Calculate proper time (ship time) for acceleration phase
    tau_acc = C/proper_acceleration * math.asinh(proper_acceleration * distance_m/(2 * C * C))
    
    # Calculate coordinate time (Earth time) for acceleration phase
    t_acc = C/proper_acceleration * math.sinh(proper_acceleration * tau_acc/C)
    
    # Calculate final velocity (at midpoint)
    v_max = C * math.tanh(proper_acceleration * tau_acc/C)
    
    # Total proper time (ship time) including deceleration
    tau_total = 2 * tau_acc
    
    # Total coordinate time (Earth time) including deceleration
    t_total = 2 * t_acc
    
    return tau_total, t_total, v_max

def calculate_relativistic_coast(distance_m, velocity, proper_acceleration, burn_time):
    """Calculate relativistic trajectory with coasting phase"""
    gamma = calculate_lorentz_factor(velocity)
    
    # Distance covered during acceleration/deceleration
    s_burn = C * C / proper_acceleration * (gamma - 1)
    
    # Remaining distance for coasting
    s_coast = distance_m - 2 * s_burn
    
    # Time for coasting phase (Earth frame)
    t_coast = s_coast / velocity
    
    # Proper time for coasting (ship frame)
    tau_coast = t_coast / gamma
    
    # Total times including acceleration and deceleration
    tau_total = 2 * burn_time + tau_coast
    t_total = 2 * (C/proper_acceleration * math.sinh(proper_acceleration * burn_time/C)) + t_coast
    
    return tau_total, t_total

def calculate_mission_parameters(dry_mass_tons, mass_ratio, distance_ly):
    """Calculate complete relativistic mission parameters with feasibility checks"""
    dry_mass_kg = dry_mass_tons * 1000
    initial_mass_kg = dry_mass_kg * mass_ratio
    distance_m = distance_ly * LY_TO_M
    
    # Calculate available delta-v
    available_dv = calculate_relativistic_deltav(EXHAUST_V, mass_ratio)
    
    # Calculate burn time based on fuel mass and mass flow
    fuel_mass_kg = initial_mass_kg - dry_mass_kg
    max_burn_time = fuel_mass_kg / ENGINE_PARAMS['total_mass_flow']
    
    # Calculate proper acceleration using initial mass
    proper_acceleration = calculate_proper_acceleration(
        ENGINE_PARAMS['total_thrust'], initial_mass_kg
    )
    
    # Calculate ideal brachistochrone trajectory
    tau_ideal, t_ideal, v_max = calculate_relativistic_brachistochrone(
        distance_m, proper_acceleration
    )
    
    # Required burn time for full brachistochrone
    required_burn_time = tau_ideal / 2
    
    if max_burn_time >= required_burn_time:
        # Full brachistochrone possible
        ship_time = tau_ideal
        earth_time = t_ideal
        coast_time = 0
        actual_burn_time = required_burn_time
        max_velocity = v_max
    else:
        # Must include coasting phase
        burn_velocity = calculate_relativistic_velocity(proper_acceleration, max_burn_time/2)
        ship_time, earth_time = calculate_relativistic_coast(
            distance_m, burn_velocity, proper_acceleration, max_burn_time/2
        )
        coast_time = ship_time - max_burn_time
        actual_burn_time = max_burn_time
        max_velocity = burn_velocity
    
    # Calculate required delta-v using relativistic velocity addition
    required_dv = 2 * C * math.atanh(max_velocity/C)
    
    # Check feasibility
    mission_feasible = required_dv <= available_dv and max_velocity < C
    
    return {
        'ship_time': ship_time,
        'earth_time': earth_time,
        'burn_time': actual_burn_time,
        'coast_time': coast_time,
        'max_velocity': max_velocity,
        'proper_acceleration': proper_acceleration,
        'available_dv': available_dv,
        'required_dv': required_dv,
        'feasible': mission_feasible,
        'gamma_max': calculate_lorentz_factor(max_velocity)
    }

def generate_results():
    """Generate results for all ship configurations and destinations"""
    results = []
    mass_ratio = 2  # Starting point - could be optimized per mission
    
    for config_name, dry_mass in SHIP_CONFIGS.items():
        for dest, dist in DESTINATIONS.items():
            params = calculate_mission_parameters(dry_mass, mass_ratio, dist)
            
            if not params['feasible']:
                continue
                
            results.append({
                'Config': config_name,
                'Dry Mass (tons)': f"{dry_mass:,}",
                'Total Mass (tons)': f"{int(dry_mass * mass_ratio):,}",
                'Destination': dest,
                'Distance (ly)': dist,
                'Proper Acceleration (g)': f"{(params['proper_acceleration']/G):.3f}",
                'Ship Time': format_duration(params['ship_time']),
                'Earth Time': format_duration(params['earth_time']),
                'Time Dilation Factor': f"{params['gamma_max']:.1f}",
                'Burn Time': format_duration(params['burn_time']),
                'Coast Time': format_duration(params['coast_time']),
                'Max Velocity (%c)': f"{(params['max_velocity']/C*100):.1f}",
                'Delta-v Required (%c)': f"{(params['required_dv']/C*100):.1f}",
                'Delta-v Available (%c)': f"{(params['available_dv']/C*100):.1f}"
            })
    
    return results

def save_to_csv(data, base_filename='relativistic_brachistochrone'):
    """Save results to CSV file with timestamp in exports folder"""
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
    
    print("\nMission Results (Feasible Missions Only):")
    current_config = ""
    for r in results:
        if r['Config'] != current_config:
            current_config = r['Config']
            print(f"\n{current_config} Configuration ({r['Dry Mass (tons)']} tons dry mass):")
            print("-" * 120)
            print(f"{'Destination':<15} | {'Accel (g)':<10} | {'Ship Time':<15} | "
                  f"{'Earth Time':<15} | {'γ factor':<8} | {'Max Speed':<10}")
            print("-" * 120)
        
        print(f"{r['Destination']:<15} | {r['Proper Acceleration (g)']:<10} | "
              f"{r['Ship Time']:<15} | {r['Earth Time']:<15} | "
              f"{r['Time Dilation Factor']:<8} | {r['Max Velocity (%c)']:>5}% c")

if __name__ == "__main__":
    results = generate_results()
    save_to_csv(results)
    print_summary(results)