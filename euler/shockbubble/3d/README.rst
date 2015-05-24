
.. _apps_euler_shockbubble_3d:

3D shock-bubble intereaction
==============================


Shock-bubble interaction solved with 3-dimensional axisymmetric Euler
equations using AMR.

A spherical bubble of gas is hit by a shock wave.  
The same gas is inside and outside the bubble (ideal gas with gamma = 1.4).
The gas inside the bubble has a lower density but the same pressure
initially as the gas outside.  Parameters are specified in `setrun.py`.

A passive tracer is also advected to show the motion of the gas originally inside
the bubble.

Version history:  
----------------

- This version updated for Clawpack 5.3.0 but currently gives an error.

- 28 Dec 2014: 

  - Updated `Makefile` to include dimensional splitting 
    option introduced in 5.3.
  - Moved from `amrclaw/examples/euler_3d_shockbubble` to
    `apps/euler/shockbubble/3d`

