
.. _apps_euler_shockbubble_2d_axisym:

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

Version history:  
----------------

- 29 May 2019: This version works with Clawpack 5.6.0 

- 28 Dec 2014: 

  - Updated `Makefile` to include dimensional splitting 
    option introduced in 5.3.
  - Moved from `apps/euler_2d_shockbubble` to `apps/euler/shockbubble/2d_axisym`

