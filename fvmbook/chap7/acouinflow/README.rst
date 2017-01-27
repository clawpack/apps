
.. _fvmbook_chap7_acouinflow:

Inflow BCs for acoustics
------------------------------------------

Acoustics equations with zero initial conditions, inflow at x=0, solid wall
at x=1.


The inflow boundary conditions are set in `bc1.f`  to be an incoming
wave of strength :math:`0.5*\sin(\omega t)`. The value of omega is specified in
`setrun.py`.

Note that after time :math:`2\pi/\omega` the boundary conditions at the left are
replaced by extrapolation (outflow) boundary conditions.



    
Example [book/chap7/acouinflow] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.
        
Converted to Clawpack 5.4.0 form in 2017.

