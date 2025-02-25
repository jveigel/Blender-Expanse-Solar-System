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

## Brachistochrone Travel Times (1/3g)

## Travel Time Matrix

*Travel time ranges (min-max)*

| From → To | Mercury | Venus | Earth | Mars | Ceres | Jupiter | Saturn | Uranus | Neptune |
|-----------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| **Mercury** | - | 2d 11h-5d 9h | 3d 13h-6d 0h | 4d 17h-7d 5h | 7d 3h-9d 4h | 10d 11h-12d 1h | 14d 12h-16d 2h | 20d 23h-22d 10h | 26d 19h-27d 12h |
| **Venus** | 2d 11h-5d 9h | - | 2d 12h-6d 13h | 4d 0h-7d 15h | 6d 16h-9d 12h | 10d 4h-12d 7h | 14d 6h-16d 7h | 20d 19h-22d 14h | 26d 16h-27d 15h |
| **Earth** | 3d 13h-6d 0h | 2d 12h-6d 13h | - | 2d 23h-8d 2h | 6d 3h-9d 21h | 9d 19h-12d 14h | 14d 0h-16d 12h | 20d 15h-22d 17h | 26d 13h-27d 18h |
| **Mars** | 4d 17h-7d 5h | 4d 0h-7d 15h | 2d 23h-8d 2h | - | 4d 15h-10d 16h | 8d 23h-13d 5h | 13d 10h-17d 0h | 20d 5h-23d 2h | 26d 6h-28d 1h |
| **Ceres** | 7d 3h-9d 4h | 6d 16h-9d 12h | 6d 3h-9d 21h | 4d 15h-10d 16h | - | 6d 22h-14d 9h | 12d 4h-17d 22h | 19d 10h-23d 18h | 25d 15h-28d 15h |
| **Jupiter** | 10d 11h-12d 1h | 10d 4h-12d 7h | 9d 19h-12d 14h | 8d 23h-13d 5h | 6d 22h-14d 9h | - | 9d 9h-19d 13h | 17d 19h-25d 0h | 24d 10h-29d 16h |
| **Saturn** | 14d 12h-16d 2h | 14d 6h-16d 7h | 14d 0h-16d 12h | 13d 10h-17d 0h | 12d 4h-17d 22h | 9d 9h-19d 13h | - | 14d 5h-27d 5h | 21d 22h-31d 13h |
| **Uranus** | 20d 23h-22d 10h | 20d 19h-22d 14h | 20d 15h-22d 17h | 20d 5h-23d 2h | 19d 10h-23d 18h | 17d 19h-25d 0h | 14d 5h-27d 5h | - | 15d 10h-35d 4h |
| **Neptune** | 26d 19h-27d 12h | 26d 16h-27d 15h | 26d 13h-27d 18h | 26d 6h-28d 1h | 25d 15h-28d 15h | 24d 10h-29d 16h | 21d 22h-31d 13h | 15d 10h-35d 4h | - |

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

# Brachistochrone Travel Times (1/3g)

| Route | Min Time | Max Time | Min dv | Max dv |
|--------|-----------|-----------|---------|--------|
| Mercury -> Venus | 2d 11h | 5d 9h | 700 | 1,528 |
| Venus -> Earth | 2d 12h | 6d 13h | 706 | 1,847 |
| Earth -> Mars | 2d 23h | 8d 2h | 844 | 2,290 |
| Mercury -> Earth | 3d 13h | 6d 0h | 1,004 | 1,703 |
| Venus -> Mars | 4d 0h | 7d 15h | 1,130 | 2,163 |
| Mars -> Ceres | 4d 15h | 10d 16h | 1,316 | 3,013 |
| Mercury -> Mars | 4d 17h | 7d 5h | 1,337 | 2,042 |
| Earth -> Ceres | 6d 3h | 9d 21h | 1,732 | 2,794 |
| Venus -> Ceres | 6d 16h | 9d 12h | 1,888 | 2,691 |
| Ceres -> Jupiter | 6d 22h | 14d 9h | 1,964 | 4,060 |
| Mercury -> Ceres | 7d 3h | 9d 4h | 2,019 | 2,595 |
| Mars -> Jupiter | 8d 23h | 13d 5h | 2,534 | 3,731 |
| Jupiter -> Saturn | 9d 9h | 19d 13h | 2,647 | 5,519 |
| Earth -> Jupiter | 9d 19h | 12d 14h | 2,773 | 3,557 |
| Venus -> Jupiter | 10d 4h | 12d 7h | 2,873 | 3,477 |
| Mercury -> Jupiter | 10d 11h | 12d 1h | 2,960 | 3,403 |
| Ceres -> Saturn | 12d 4h | 17d 22h | 3,443 | 5,061 |
| Mars -> Saturn | 13d 10h | 17d 0h | 3,797 | 4,801 |
| Earth -> Saturn | 14d 0h | 16d 12h | 3,960 | 4,667 |
| Saturn -> Uranus | 14d 5h | 27d 5h | 4,016 | 7,682 |
| Venus -> Saturn | 14d 6h | 16d 7h | 4,031 | 4,606 |
| Mercury -> Saturn | 14d 12h | 16d 2h | 4,094 | 4,550 |
| Uranus -> Neptune | 15d 10h | 35d 4h | 4,355 | 9,936 |
| Jupiter -> Uranus | 17d 19h | 25d 0h | 5,025 | 7,063 |
| Ceres -> Uranus | 19d 10h | 23d 18h | 5,486 | 6,711 |
| Mars -> Uranus | 20d 5h | 23d 2h | 5,715 | 6,517 |
| Earth -> Uranus | 20d 15h | 22d 17h | 5,825 | 6,419 |
| Venus -> Uranus | 20d 19h | 22d 14h | 5,873 | 6,375 |
| Mercury -> Uranus | 20d 23h | 22d 10h | 5,917 | 6,335 |
| Saturn -> Neptune | 21d 22h | 31d 13h | 6,197 | 8,905 |
| Jupiter -> Neptune | 24d 10h | 29d 16h | 6,894 | 8,377 |
| Ceres -> Neptune | 25d 15h | 28d 15h | 7,237 | 8,082 |
| Mars -> Neptune | 26d 6h | 28d 1h | 7,412 | 7,922 |
| Earth -> Neptune | 26d 13h | 27d 18h | 7,497 | 7,842 |
| Venus -> Neptune | 26d 16h | 27d 15h | 7,534 | 7,806 |
| Mercury -> Neptune | 26d 19h | 27d 12h | 7,568 | 7,773 |