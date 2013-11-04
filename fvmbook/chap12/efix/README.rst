
.. _fvmbook_chap12/efix:

Entropy Fix Examples with Burger's Eqn
--------------------------------------------

    
Example [book/chap12/efix] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.

Burgers' equation with a transonic rarefaction wave.

Comparison of results obtained with or without the entropy fix.
This is set in the Riemann solver rp1_burgers.f90 by modifying the variable efix.

Note: also try changing mx in setrun.py
to an odd value (e.g. 61 instead of 60).
Then there is one grid cell with the value 0.5 at x=0 and a different
weak solution is obtained.

Note: The solution also looks much smoother if you set order=2 in setrun.py
instead of order=1. 

