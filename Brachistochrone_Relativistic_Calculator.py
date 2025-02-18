"""
Relativistic Brachistochrone Calculator for Interstellar Travel Times

This module calculates travel times from Sol to other stars using relativistic
brachistochrone trajectories under different acceleration scenarios.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple
import csv
import math

def days_to_dhm(days: float) -> str:
    """Convert decimal days to days, hours, minutes string."""
    total_hours = days * 24
    d = int(total_hours // 24)
    h = int(total_hours % 24)
    m = int((total_hours % 1) * 60)
    return f"{d}d {h}h {m}m"

# Physical constants
@dataclass(frozen=True)
class Constants:
    G_MULTIPLIER: float = 0.0098  # km/s² per g
    G: float = 0.0098  # km/s² (1g acceleration)
    G_0_3: float = 0.00294  # km/s² (0.3g acceleration)
    AU_TO_KM: float = 1.496e8  # kilometers per AU
    LIGHT_YEAR_TO_AU: float = 63241.1  # AU per light year
    C: float = 299792.458  # Speed of light in km/s

# Star data
@dataclass(frozen=True)
class Star:
    distance_ly: float  # Light years from Sol
    name: str  # Common name
    description: str = ""  # Optional description or notes

STARS: Dict[str, Star] = {
    'Proxima Centauri': Star(4.246, "Proxima Centauri", "Closest star to Sol"),
    'Alpha Centauri A': Star(4.37, "Alpha Centauri A", "G2V star similar to Sol"),
    'Alpha Centauri B': Star(4.37, "Alpha Centauri B", "K1V orange dwarf star"),
    'Barnard\'s Star': Star(5.958, "Barnard's Star", "Red dwarf with high proper motion"),
    'Wolf 359': Star(7.9, "Wolf 359", "Red dwarf in Leo"),
    'Sirius': Star(8.611, "Sirius A", "Brightest star in Earth's night sky"),
    'Tau Ceti': Star(11.912, "Tau Ceti", "Similar to Sol, possibly habitable planets"),
    'Epsilon Eridani': Star(10.475, "Epsilon Eridani", "Young K2V star with planetary system")
}

@dataclass
class TravelMetrics:
    """Container for relativistic travel calculation results."""
    distance_ly: float  # Light years
    distance_km: float  # Kilometers
    time_ship: float  # days (proper time)
    time_earth: float  # days (coordinate time)
    max_velocity_c: float  # fraction of light speed
    delta_v: float  # km/s
    time_years_ship: float  # years for human readability
    time_years_earth: float  # years for human readability

class RelativisticCalculator:
    """Handles calculations for relativistic brachistochrone trajectories."""
    
    def __init__(self, constants: Constants = Constants()):
        self.constants = constants

    def calculate_relativistic_time(self, distance_km: float, 
                                  acceleration_kms2: float) -> Tuple[float, float]:
        """
        Calculate relativistic travel time for given distance and acceleration.
        Returns tuple of (proper time, coordinate time) in seconds.
        """
        c = self.constants.C
        a = acceleration_kms2
        
        # Proper time (time experienced on ship)
        tau = (c/a) * math.acosh(1 + (a*distance_km)/(c*c))
        
        # Coordinate time (time measured by Earth)
        t = (c/a) * math.sinh(math.acosh(1 + (a*distance_km)/(c*c)))
        
        return tau, t

    def calculate_max_velocity(self, proper_time_seconds: float, 
                             acceleration_kms2: float) -> float:
        """Calculate relativistic maximum velocity as fraction of c."""
        v = math.tanh(acceleration_kms2 * proper_time_seconds / 
                     (2 * self.constants.C)) * self.constants.C
        return v / self.constants.C  # Return as fraction of c

    def calculate_total_deltav(self, max_velocity_kms: float) -> float:
        """Calculate total delta-v required for the mission."""
        return 2 * max_velocity_kms

    def calculate_metrics(self, star: Star, acceleration: float) -> TravelMetrics:
        """Calculate complete relativistic travel metrics from Sol to star."""
        # Convert distance to kilometers
        distance_au = star.distance_ly * self.constants.LIGHT_YEAR_TO_AU
        distance_km = distance_au * self.constants.AU_TO_KM
        
        # Calculate travel times
        ship_time, earth_time = self.calculate_relativistic_time(
            distance_km, acceleration)
        
        # Convert times to days
        ship_days = ship_time / 86400
        earth_days = earth_time / 86400
        
        # Calculate maximum velocity (as fraction of c)
        max_velocity_c = self.calculate_max_velocity(ship_time, acceleration)
        
        # Calculate delta-v
        delta_v = self.calculate_total_deltav(max_velocity_c * self.constants.C)
        
        return TravelMetrics(
            distance_ly=star.distance_ly,
            distance_km=distance_km,
            time_ship=ship_days,
            time_earth=earth_days,
            max_velocity_c=max_velocity_c,
            delta_v=delta_v,
            time_years_ship=ship_days/365.25,
            time_years_earth=earth_days/365.25
        )

class DataFormatter:
    """Handles data formatting and file output."""
    
    @staticmethod
    def generate_csv_row(star_name: str, metrics_1g: TravelMetrics, 
                        metrics_03g: TravelMetrics, star: Star) -> List:
        """Generate a single CSV row."""
        return [
            star_name,
            star.description,
            round(star.distance_ly, 3),
            round(metrics_1g.distance_km, 0),
            round(metrics_1g.time_ship, 3),
            round(metrics_1g.time_earth, 3),
            round(metrics_1g.time_years_ship, 2),
            round(metrics_1g.time_years_earth, 2),
            round(metrics_1g.max_velocity_c * 100, 2),
            round(metrics_1g.delta_v, 2),
            round(metrics_03g.time_ship, 3),
            round(metrics_03g.time_earth, 3),
            round(metrics_03g.time_years_ship, 2),
            round(metrics_03g.time_years_earth, 2),
            round(metrics_03g.max_velocity_c * 100, 2),
            round(metrics_03g.delta_v, 2)
        ]

    @staticmethod
    def format_markdown_row(star_name: str, metrics: TravelMetrics) -> str:
        """Format a single markdown table row."""
        return (f"| {star_name} | {metrics.distance_ly:.2f} | "
                f"{days_to_dhm(metrics.time_ship)} | {days_to_dhm(metrics.time_earth)} | "
                f"{metrics.max_velocity_c*100:.1f}% | {metrics.delta_v:,.0f} |")

def main():
    """Main execution function."""
    calculator = RelativisticCalculator()
    formatter = DataFormatter()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Calculate routes
    routes = []
    headers = [
        'star_name', 'description', 'distance_light_years', 'distance_km',
        'time_ship_days_1g', 'time_earth_days_1g',
        'time_ship_years_1g', 'time_earth_years_1g',
        'max_velocity_c_1g', 'delta_v_kms_1g',
        'time_ship_days_0_3g', 'time_earth_days_0_3g',
        'time_ship_years_0_3g', 'time_earth_years_0_3g',
        'max_velocity_c_0_3g', 'delta_v_kms_0_3g'
    ]
    
    # Sort stars by distance
    sorted_stars = sorted(STARS.items(), key=lambda x: x[1].distance_ly)
    
    # Generate all routes from Sol
    print("\nRelativistic Travel Times from Sol:\n")
    print("| Star | Distance (ly) | Ship Time (1g) | Earth Time (1g) | Max Velocity | Delta-v (km/s) |")
    print("|------|--------------|----------------|-----------------|--------------|----------------|")
    
    for star_name, star in sorted_stars:
        metrics_1g = calculator.calculate_metrics(star, Constants.G)
        metrics_03g = calculator.calculate_metrics(star, Constants.G_0_3)
        
        # Add to CSV data
        row = formatter.generate_csv_row(
            star_name, metrics_1g, metrics_03g, star)
        routes.append(row)
        
        # Print markdown table row
        print(formatter.format_markdown_row(star_name, metrics_1g))
    
    # Write CSV output
    csv_filename = f"exports/relativistic_stellar_{timestamp}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(routes)
    
    print(f"\nCSV data saved to: {csv_filename}")
    print(f"Total routes calculated: {len(routes)}")

if __name__ == "__main__":
    main()