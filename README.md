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

## Brachistochrone Travel Times (0.3g)

*Travel time ranges (min-max)*

| From → To | Mercury | Venus | Earth | Mars | Ceres | Jupiter | Saturn | Uranus | Neptune |
|-----------|---------|-------|-------|------|-------|---------|--------|--------|---------|
| **Mercury** | - | 2d14h-5d16h | 3d18h-6d8h | 4d23h-7d15h | 7d12h-9d16h | 11d1h-12d17h | 15d6h-16d23h | 22d2h-23d15h | 28d6h-29d0h |
| **Venus** | 2d14h-5d16h | - | 2d15h-6d21h | 4d5h-8d1h | 7d1h-10d1h | 10d17h-12d23h | 15d1h-17d4h | 21d22h-23d19h | 28d3h-29d3h |
| **Earth** | 3d18h-6d8h | 2d15h-6d21h | - | 3d3h-8d13h | 6d11h-10d10h | 10d8h-13d6h | 14d18h-17d10h | 21d18h-23d23h | 27d23h-29d6h |
| **Mars** | 4d23h-7d15h | 4d5h-8d1h | 3d3h-8d13h | - | 4d21h-11d6h | 9d11h-13d22h | 14d4h-17d22h | 21d8h-24d8h | 27d16h-29d14h |
| **Ceres** | 7d12h-9d16h | 7d1h-10d1h | 6d11h-10d10h | 4d21h-11d6h | - | 7d8h-15d3h | 12d20h-18d21h | 20d11h-25d1h | 27d0h-30d4h |
| **Jupiter** | 11d1h-12d17h | 10d17h-12d23h | 10d8h-13d6h | 9d11h-13d22h | 7d8h-15d3h | - | 9d21h-20d14h | 18d18h-26d9h | 25d17h-31d6h |
| **Saturn** | 15d6h-16d23h | 15d1h-17d4h | 14d18h-17d10h | 14d4h-17d22h | 12d20h-18d21h | 9d21h-20d14h | - | 14d23h-28d16h | 23d3h-33d6h |
| **Uranus** | 22d2h-23d15h | 21d22h-23d19h | 21d18h-23d23h | 21d8h-24d8h | 20d11h-25d1h | 18d18h-26d9h | 14d23h-28d16h | - | 16d6h-37d2h |
| **Neptune** | 28d6h-29d0h | 28d3h-29d3h | 27d23h-29d6h | 27d16h-29d14h | 27d0h-30d4h | 25d17h-31d6h | 23d3h-33d6h | 16d6h-37d2h | - |

## Brachistochrone Travel Times (0.3g) - Sorted by Delta-v

| Route | Min Time | Max Time | Min dv | Max dv |
|--------|-----------|-----------|---------|--------|
| Mercury -> Venus | 2d 14h | 5d 16h | 665 | 1,450 |
| Venus -> Earth | 2d 15h | 6d 21h | 670 | 1,752 |
| Earth -> Mars | 3d 3h | 8d 13h | 800 | 2,173 |
| Mercury -> Earth | 3d 18h | 6d 8h | 953 | 1,616 |
| Venus -> Mars | 4d 5h | 8d 1h | 1,072 | 2,052 |
| Mars -> Ceres | 4d 21h | 11d 6h | 1,248 | 2,858 |
| Mercury -> Mars | 4d 23h | 7d 15h | 1,268 | 1,937 |
| Earth -> Ceres | 6d 11h | 10d 10h | 1,643 | 2,651 |
| Venus -> Ceres | 7d 1h | 10d 1h | 1,791 | 2,553 |
| Ceres -> Jupiter | 7d 8h | 15d 3h | 1,863 | 3,852 |
| Mercury -> Ceres | 7d 12h | 9d 16h | 1,915 | 2,462 |
| Mars -> Jupiter | 9d 11h | 13d 22h | 2,404 | 3,540 |
| Jupiter -> Saturn | 9d 21h | 20d 14h | 2,511 | 5,236 |
| Earth -> Jupiter | 10d 8h | 13d 6h | 2,630 | 3,375 |
| Venus -> Jupiter | 10d 17h | 12d 23h | 2,725 | 3,299 |
| Mercury -> Jupiter | 11d 1h | 12d 17h | 2,808 | 3,228 |
| Ceres -> Saturn | 12d 20h | 18d 21h | 3,266 | 4,801 |
| Mars -> Saturn | 14d 4h | 17d 22h | 3,602 | 4,554 |
| Earth -> Saturn | 14d 18h | 17d 10h | 3,757 | 4,427 |
| Saturn -> Uranus | 14d 23h | 28d 16h | 3,810 | 7,288 |
| Venus -> Saturn | 15d 1h | 17d 4h | 3,824 | 4,369 |
| Mercury -> Saturn | 15d 6h | 16d 23h | 3,884 | 4,317 |
| Uranus -> Neptune | 16d 6h | 37d 2h | 4,132 | 9,426 |
| Jupiter -> Uranus | 18d 18h | 26d 9h | 4,767 | 6,701 |
| Ceres -> Uranus | 20d 11h | 25d 1h | 5,205 | 6,367 |
| Mars -> Uranus | 21d 8h | 24d 8h | 5,422 | 6,183 |
| Earth -> Uranus | 21d 18h | 23d 23h | 5,526 | 6,090 |
| Venus -> Uranus | 21d 22h | 23d 19h | 5,572 | 6,048 |
| Mercury -> Uranus | 22d 2h | 23d 15h | 5,613 | 6,010 |
| Saturn -> Neptune | 23d 3h | 33d 6h | 5,879 | 8,448 |
| Jupiter -> Neptune | 25d 17h | 31d 6h | 6,540 | 7,947 |
| Ceres -> Neptune | 27d 0h | 30d 4h | 6,865 | 7,668 |
| Mars -> Neptune | 27d 16h | 29d 14h | 7,031 | 7,516 |
| Earth -> Neptune | 27d 23h | 29d 6h | 7,112 | 7,439 |
| Venus -> Neptune | 28d 3h | 29d 3h | 7,148 | 7,405 |
| Mercury -> Neptune | 28d 6h | 29d 0h | 7,180 | 7,374 |