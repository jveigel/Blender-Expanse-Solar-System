If you know the desired acceleration of your spacecraft (generally one g or 9.81 m/s2) and wish to calculate the transit time, the Brachistochrone equation is

T = 2 * sqrt[ D/A ]

(ed note: pay attention, it is D DIVIDED by A)

where

T = transit time (seconds)
D = distance (meters)
A = acceleration (m/s2)
sqrt[x] = square root of x
Remember that

AU * 1.49e11 = meters
1 g of acceleration = 9.81 m/s2
one-tenth g of acceleration = 0.981 m/s2
one one-hundredth g of acceleration = 0.0981 m/s2
Divide time in seconds by

3600 for hours
86400 for days
2592000 for (30 day) months
31536000 for years

"Colony Sphere" from a 1959 poster. Everything else in the poster has been "borrowed" from other sources, so one of suspicious mind would think this might have been "inspired" by the colony torchship "Mayflower" in Heinlein's FARMER IN THE SKY.
Timothy Charters worked out the following equation. It is the above transit time equation for weaker spacecraft that have to coast during the midpoint

T = ((D - (A * t^2)) / (A * t)) + (2*t)

where

T = transit time (seconds)
D = distance (meters)
A = acceleration (m/s2)
t = duration of acceleration phase (seconds), just the acceleration phase only, NOT the acceleration+deceleration phase.
Note that the coast duration time is of course = T - (2*t)

ACCELERATION given distance and desired transit time

link for sharing If you know the desired transit time and wish to calculate the required acceleration, the equation is

A = (4 * D) / T2

Keep in mind that prolonged periods of acceleration a greater than one g is very bad for the crew's health.

Yes, it is supposed to be 2 * sqrt[ D/A ], NOT sqrt[ 2 * D/A ]

Don't be confused. You might think that the Brachistochrone equation should be T = sqrt[ 2 * D/A ] instead of T = 2 * sqrt[ D/A ], since your physics textbook states that D = 0.5 * A * T^2. The confusion is because the D in the physics book refers to the mid-way distance, not the total distance.

This changes the physics book equation from

D = 0.5 * A * t^2

to

D * 0.5 = 0.5 * A * t^2

Solving for t gives us t = sqrt(D/A) where t is the time to the mid-way distance. Since it takes an equal amount of time to slow down, the total trip time T is twice that or T = 2 * sqrt( D/A ). Which is the Brachistochrone equation given above.