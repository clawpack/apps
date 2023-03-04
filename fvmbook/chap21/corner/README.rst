.. _fvmbook_chap21_corner:

2D acoustics with variable coefficients
--------------------------------------------------


Example [book/chap21/corner] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems <http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2023.
        
Two materials with a single interface, specified in `fdisc.f`
(which is called from the library routine `$CLAW/classic/src/2d/cellave.f`
to compute the fraction of each grid cell lying in the left and right states).

`Figure showing interface <interface.png>`__ created by `makegridfig.py` 

The sound speed and impedance are stored in the aux array, specified in
`setaux.f`.
For cells cut by the interface, the arithmetic average of rho and harmonic
average of the bulk modulus are used to determine these parameters for this
cell.
