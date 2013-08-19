
.. _fvmbook_chap10/tvb:

TVB Method of Shu on Advection
------------------------------------------

    
Example [book/chapX/XX] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems <http://www.clawpack.org/book>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.
        
This directory contains a modified limiter.f function which implements the
TVB method of Shu as an extension of the second-order minmod method.

The value of phiM, set in setrun.py, 
should be chosen as an approximation to
q_{xx} at the extrema to be captured.   The grid should be fine enough that 
phiM*dx is small or the method will be dispersive.  

For the wave-packet problem used here, you might experiment with:
  1.  phiM = 6500 or other values 
  2. different resolutions, such as 400 or 800 points
  3. different limiters besides minmod (which may work poorly!)

