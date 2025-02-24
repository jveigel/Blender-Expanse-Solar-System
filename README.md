# Blender-Solar-System





## Scripts
`Blender_Orbits_Jupiter.py`
`Blender_Orbits_Saturn.py`
`Blender_Orbits_SolarSystem.py`

Python scripts to create accurate orbits in Blender.

`SolarSystemScale8k_Accurate.py`

Creates an image file of scale accurate orbits at about 10,000 px.

`BrachistochroneCalc.py`

Saves a csv and markdown file with the results of the brachistochrone trajectories at 1g and 0.3g.

`Brachistochrone_Relativistic_Calculator_Epstein.py`

Attempts to estimate the interstellar travel times using the relativistic brachistochrone equation for the Nauvoo from the Expanse. It is not very accurate, canonically or scientifically.

##

# Brachistochrone Travel Times (0.3g)

*Days (min-max) | Δv (km/s)*

| From→To | Mercury | Venus | Earth | Mars | Ceres | Jupiter | Saturn | Uranus | Neptune |
|---------|---------|-------|-------|------|-------|---------|--------|--------|---------|
| **Mercury** | - | 2.6-5.7  1,450 | 3.8-6.3  1,616 | 4.9-7.6  1,937 | 7.5-9.7  2,462 | 11.0-12.7  3,228 | 15.3-16.9  4,317 | 22.1-23.6  6,010 | 28.3-29.0  7,374 |
| **Venus** | 2.6-5.7  1,450 | - | 2.6-6.9  1,752 | 4.2-8.0  2,052 | 7.0-10.0  2,553 | 10.7-12.9  3,299 | 15.0-17.2  4,369 | 21.9-23.8  6,048 | 28.1-29.1  7,405 |
| **Earth** | 3.8-6.3  1,616 | 2.6-6.9  1,752 | - | 3.1-8.5  2,173 | 6.5-10.4  2,651 | 10.3-13.3  3,375 | 14.8-17.4  4,427 | 21.8-23.9  6,090 | 27.9-29.3  7,439 |
| **Mars** | 4.9-7.6  1,937 | 4.2-8.0  2,052 | 3.1-8.5  2,173 | - | 4.9-11.3  2,858 | 9.5-13.9  3,540 | 14.2-17.9  4,554 | 21.3-24.3  6,183 | 27.7-29.6  7,516 |
| **Ceres** | 7.5-9.7  2,462 | 7.0-10.0  2,553 | 6.5-10.4  2,651 | 4.9-11.3  2,858 | - | 7.3-15.1  3,852 | 12.8-18.9  4,801 | 20.5-25.0  6,367 | 27.0-30.2  7,668 |
| **Jupiter** | 11.0-12.7  3,228 | 10.7-12.9  3,299 | 10.3-13.3  3,375 | 9.5-13.9  3,540 | 7.3-15.1  3,852 | - | 9.9-20.6  5,236 | 18.8-26.4  6,701 | 25.7-31.3  7,947 |
| **Saturn** | 15.3-16.9  4,317 | 15.0-17.2  4,369 | 14.8-17.4  4,427 | 14.2-17.9  4,554 | 12.8-18.9  4,801 | 9.9-20.6  5,236 | - | 14.9-28.7  7,288 | 23.1-33.1  8,448 |
| **Uranus** | 22.1-23.6  6,010 | 21.9-23.8  6,048 | 21.8-23.9  6,090 | 21.3-24.3  6,183 | 20.5-25.0  6,367 | 18.8-26.4  6,701 | 14.9-28.7  7,288 | - | 16.3-37.0  9,426 |
| **Neptune** | 28.3-29.0  7,374 | 28.1-29.1  7,405 | 27.9-29.3  7,439 | 27.7-29.6  7,516 | 27.0-30.2  7,668 | 25.7-31.3  7,947 | 23.1-33.1  8,448 | 16.3-37.0  9,426 | - |

## Brachistochrone Travel Times (0.3g) - Iterative Format

| Route | Min Time | Max Time | Delta-v (km/s) |
|--------|-----------|-----------|---------------|
| Mercury -> Venus | 2d 14h | 5d 16h | 1,450 |
| Mercury -> Earth | 3d 18h | 6d 8h | 1,616 |
| Mercury -> Mars | 4d 23h | 7d 15h | 1,937 |
| Mercury -> Ceres | 7d 12h | 9d 16h | 2,462 |
| Mercury -> Jupiter | 11d 1h | 12d 17h | 3,228 |
| Mercury -> Saturn | 15d 6h | 16d 23h | 4,317 |
| Mercury -> Uranus | 22d 2h | 23d 15h | 6,010 |
| Mercury -> Neptune | 28d 6h | 29d 0h | 7,374 |
| Venus -> Earth | 2d 15h | 6d 21h | 1,752 |
| Venus -> Mars | 4d 5h | 8d 1h | 2,052 |
| Venus -> Ceres | 7d 1h | 10d 1h | 2,553 |
| Venus -> Jupiter | 10d 17h | 12d 23h | 3,299 |
| Venus -> Saturn | 15d 1h | 17d 4h | 4,369 |
| Venus -> Uranus | 21d 22h | 23d 19h | 6,048 |
| Venus -> Neptune | 28d 3h | 29d 3h | 7,405 |
| Earth -> Mars | 3d 3h | 8d 13h | 2,173 |
| Earth -> Ceres | 6d 11h | 10d 10h | 2,651 |
| Earth -> Jupiter | 10d 8h | 13d 6h | 3,375 |
| Earth -> Saturn | 14d 18h | 17d 10h | 4,427 |
| Earth -> Uranus | 21d 18h | 23d 23h | 6,090 |
| Earth -> Neptune | 27d 23h | 29d 6h | 7,439 |
| Mars -> Ceres | 4d 21h | 11d 6h | 2,858 |
| Mars -> Jupiter | 9d 11h | 13d 22h | 3,540 |
| Mars -> Saturn | 14d 4h | 17d 22h | 4,554 |
| Mars -> Uranus | 21d 8h | 24d 8h | 6,183 |
| Mars -> Neptune | 27d 16h | 29d 14h | 7,516 |
| Ceres -> Jupiter | 7d 8h | 15d 3h | 3,852 |
| Ceres -> Saturn | 12d 20h | 18d 21h | 4,801 |
| Ceres -> Uranus | 20d 11h | 25d 1h | 6,367 |
| Ceres -> Neptune | 27d 0h | 30d 4h | 7,668 |
| Jupiter -> Saturn | 9d 21h | 20d 14h | 5,236 |
| Jupiter -> Uranus | 18d 18h | 26d 9h | 6,701 |
| Jupiter -> Neptune | 25d 17h | 31d 6h | 7,947 |
| Saturn -> Uranus | 14d 23h | 28d 16h | 7,288 |
| Saturn -> Neptune | 23d 3h | 33d 6h | 8,448 |
| Uranus -> Neptune | 16d 6h | 37d 2h | 9,426 |