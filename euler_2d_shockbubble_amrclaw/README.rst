
.. _apps_euler_2d_shockbubble_amrclaw:

2D Axisymmetric shock-bubble intereaction
==========================================


Shock-bubble interaction solved with 2-dimensional axisymmetric Euler
equations using AMR.

A circular (i.e. spherical) bubble of gas is hit by a shock wave.  
The same gas is inside and outside the bubble (ideal gas with gamma = 1.4).
The gas inside the bubble has a lower density but the same pressure
initially as the gas outside.  Parameters are specified in `setrun.py`.

A passive tracer is also advected to show the motion of the gas originally inside
the bubble.

Version:  This version works with Clawpack 5.0 -- 5.2 (?)
