"""
Brachistochrone Calculator for Interplanetary Travel Times

This module calculates travel times between planets using brachistochrone trajectories
under different acceleration scenarios.
"""

from dataclasses import dataclass
from datetime import datetime
from itertools import combinations
from typing import Dict, List, Tuple
import csv
import math

def days_to_dhm(days: float) -> str:
    """Convert decimal days to days and hours string."""
    total_hours = days * 24
    d = int(total_hours // 24)
    h = int(total_hours % 24)
    return f"{d}d {h}h"

# Physical constants
@dataclass(frozen=True)
class Constants:
    G_MULTIPLIER: float = 0.0098  # km/s² per g
    G: float = 0.0098  # km/s² (1g acceleration)
    G_0_3: float = 0.00294  # km/s² (0.3g acceleration)
    AU_TO_KM: float = 1.496e8  # kilometers per AU
    C: float = 299792.458  # Speed of light in km/s

# Planetary orbital parameters
@dataclass(frozen=True)
class Planet:
    perihelion: float  # AU
    aphelion: float  # AU

PLANETS: Dict[str, Planet] = {
    'Mercury': Planet(0.307, 0.467),
    'Venus': Planet(0.718, 0.728),
    'Earth': Planet(0.983, 1.017),
    'Mars': Planet(1.381, 1.666),
    'Ceres': Planet(2.5518, 2.9775),
    'Jupiter': Planet(4.950, 5.457),
    'Saturn': Planet(9.041, 10.124),
    'Uranus': Planet(18.375, 20.063),
    'Neptune': Planet(29.767, 30.441)
}

@dataclass
class TravelMetrics:
    """Container for travel calculation results."""
    min_distance: float  # AU
    max_distance: float  # AU
    min_time: float  # days
    max_time: float  # days
    median_time: float  # days
    delta_v: float  # km/s

class BrachistochroneCalculator:
    """Handles calculations for brachistochrone trajectories between planets."""
    
    def __init__(self, constants: Constants = Constants()):
        self.constants = constants

    def calculate_brachistochrone_time(self, distance_km: float, acceleration_kms2: float) -> float:
        """Calculate brachistochrone time for given distance and acceleration."""
        return 2 * math.sqrt(distance_km / acceleration_kms2)

    def calculate_max_velocity(self, time_seconds: float, acceleration_kms2: float) -> float:
        """Calculate maximum velocity achieved at midpoint."""
        return acceleration_kms2 * (time_seconds / 2)

    def calculate_total_deltav(self, max_velocity: float) -> float:
        """Calculate total delta-v required for the mission."""
        return 2 * max_velocity

    def get_orbital_distances(self, p1: Planet, p2: Planet) -> Tuple[float, float]:
        """Calculate minimum and maximum possible distances between two planetary orbits."""
        min_dist = max(0, max(p1.perihelion, p2.perihelion) - min(p1.aphelion, p2.aphelion))
        max_dist = p1.aphelion + p2.aphelion
        return (min_dist, max_dist)

    def calculate_median_distance(self, p1: Planet, p2: Planet) -> float:
        """Calculate median distance between two planetary orbits."""
        r1 = (p1.perihelion + p1.aphelion) / 2
        r2 = (p2.perihelion + p2.aphelion) / 2
        
        if abs(r1 - 1) < 0.1:  # If origin is Earth's orbit
            return math.sqrt(1 + r2 * r2)
        else:
            m1 = math.sqrt(1 + r1 * r1)
            m2 = math.sqrt(1 + r2 * r2)
            return abs(m2 - m1)

    def calculate_metrics(self, origin: Planet, destination: Planet,
                         acceleration: float) -> TravelMetrics:
        """Calculate complete travel metrics between two planets.
        
        Uses max_time for velocity calculations to get worst-case delta-v requirements."""
        min_dist, max_dist = self.get_orbital_distances(origin, destination)
        min_dist_km = min_dist * self.constants.AU_TO_KM
        max_dist_km = max_dist * self.constants.AU_TO_KM
        
        min_time = self.calculate_brachistochrone_time(min_dist_km, acceleration)
        max_time = self.calculate_brachistochrone_time(max_dist_km, acceleration)
        
        median_dist = self.calculate_median_distance(origin, destination)
        median_time = self.calculate_brachistochrone_time(
            median_dist * self.constants.AU_TO_KM, acceleration)
        
        max_velocity = self.calculate_max_velocity(max_time, acceleration)
        delta_v = self.calculate_total_deltav(max_velocity)
        
        return TravelMetrics(
            min_distance=min_dist,
            max_distance=max_dist,
            min_time=min_time / 86400,  # Convert to days
            max_time=max_time / 86400,
            median_time=median_time / 86400,
            delta_v=delta_v
        )

class DataFormatter:
    """Handles data formatting and file output."""
    
    @staticmethod
    def generate_csv_row(origin_name: str, dest_name: str, 
                        metrics_1g: TravelMetrics, metrics_03g: TravelMetrics,
                        origin: Planet, destination: Planet) -> List:
        """Generate a single CSV row."""
        return [
            origin_name,
            dest_name,
            round(metrics_1g.min_distance, 6),
            round(metrics_1g.max_distance, 6),
            round(metrics_1g.min_distance * Constants.AU_TO_KM, 0),
            round(metrics_1g.max_distance * Constants.AU_TO_KM, 0),
            round(metrics_1g.min_time, 3),
            round(metrics_1g.max_time, 3),
            round(metrics_1g.median_time, 3),
            round(metrics_1g.delta_v, 2),
            round(metrics_03g.min_time, 3),
            round(metrics_03g.max_time, 3),
            round(metrics_03g.median_time, 3),
            round(metrics_03g.delta_v, 2),
            origin.perihelion,
            origin.aphelion,
            destination.perihelion,
            destination.aphelion
        ]

    @staticmethod
    def format_markdown_row(name1: str, name2: str, metrics: TravelMetrics, 
                          max_velocity: float) -> str:
        """Format a single markdown table row with separated columns."""
        route = f"{name1} -> {name2}"
        min_distance = f"{metrics.min_distance * Constants.AU_TO_KM:,.0f}"
        max_distance = f"{metrics.max_distance * Constants.AU_TO_KM:,.0f}"
        min_time = days_to_dhm(metrics.min_time)
        max_time = days_to_dhm(metrics.max_time)
        median_time = days_to_dhm(metrics.median_time)
        velocity = f"{max_velocity:,.0f}"
        deltav = f"{metrics.delta_v:,.0f}"
        
        return f"| {route} | {min_distance} | {max_distance} | {min_time} | {max_time} | {median_time} | {velocity} | {deltav} |"

def main():
    """Main execution function."""
    calculator = BrachistochroneCalculator()
    formatter = DataFormatter()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Define solar system order for sorting
    planet_order = ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
    # Generate all routes
    routes = []
    headers = [
        'origin_planet', 'destination_planet',
        'min_time_days_0_3g', 'max_time_days_0_3g', 'median_time_days_0_3g',
        'min_time_days_1g', 'max_time_days_1g', 'median_time_days_1g',
        'min_distance_au', 'max_distance_au',
        'min_distance_km', 'max_distance_km',
        'max_deltav_kms_0_3g', 'max_deltav_kms_1g',
        'origin_perihelion_au', 'origin_aphelion_au',
        'destination_perihelion_au', 'destination_aphelion_au'
    ]
    
    # Generate routes in solar system order
    for origin_idx, name1 in enumerate(planet_order):
        for name2 in planet_order[origin_idx + 1:]:
            metrics_1g = calculator.calculate_metrics(
                PLANETS[name1], PLANETS[name2], Constants.G)
            metrics_03g = calculator.calculate_metrics(
                PLANETS[name1], PLANETS[name2], Constants.G_0_3)
            
            row = [
                name1, name2,
                round(metrics_03g.min_time, 3),
                round(metrics_03g.max_time, 3),
                round(metrics_03g.median_time, 3),
                round(metrics_1g.min_time, 3),
                round(metrics_1g.max_time, 3),
                round(metrics_1g.median_time, 3),
                round(metrics_1g.min_distance, 6),
                round(metrics_1g.max_distance, 6),
                round(metrics_1g.min_distance * Constants.AU_TO_KM, 0),
                round(metrics_1g.max_distance * Constants.AU_TO_KM, 0),
                round(metrics_03g.delta_v, 2),
                round(metrics_1g.delta_v, 2),
                PLANETS[name1].perihelion,
                PLANETS[name1].aphelion,
                PLANETS[name2].perihelion,
                PLANETS[name2].aphelion
            ]
            routes.append(row)
    
    # Add Alpha Centauri routes from each planet
    for origin in planet_order:
        metrics_1g = calculator.calculate_metrics(
            PLANETS[origin], PLANETS['Alpha Centauri'], Constants.G)
        metrics_03g = calculator.calculate_metrics(
            PLANETS[origin], PLANETS['Alpha Centauri'], Constants.G_0_3)
        
        row = [
            origin, 'Alpha Centauri',
            round(metrics_03g.min_time, 3),
            round(metrics_03g.max_time, 3),
            round(metrics_03g.median_time, 3),
            round(metrics_1g.min_time, 3),
            round(metrics_1g.max_time, 3),
            round(metrics_1g.median_time, 3),
            round(metrics_1g.min_distance, 6),
            round(metrics_1g.max_distance, 6),
            round(metrics_1g.min_distance * Constants.AU_TO_KM, 0),
            round(metrics_1g.max_distance * Constants.AU_TO_KM, 0),
            round(metrics_03g.delta_v, 2),
            round(metrics_1g.delta_v, 2),
            PLANETS[origin].perihelion,
            PLANETS[origin].aphelion,
            PLANETS['Alpha Centauri'].perihelion,
            PLANETS['Alpha Centauri'].aphelion
        ]
        routes.append(row)
    
    # Write CSV output
    csv_filename = f"exports/brachistochrone_extended_{timestamp}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(routes)
    
    print(f"CSV data saved to: {csv_filename}")
    print(f"Total routes calculated: {len(routes)}")

if __name__ == "__main__":
    main()