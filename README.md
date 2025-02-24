# Blender-Solar-System



## Brachistochrone Travel Times (0.3g)

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

