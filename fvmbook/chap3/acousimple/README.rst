.. For a more readable version with a browsable list of files,
.. execute "make .htmls" and open README.html in a browser

.. _fvmbook_chap3/acousimple:

1D Acoustics with simple waves 
------------------------------------------

    
Example [book/chap3/acousimple]
to accompany Figure 3.1 of the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.
        
Added plots of characteristic variables in 2023 using v5.9.0

1d acoustics in a constant medium.

.. math:: q_t + A q_x = 0

where

.. math:: q(x,t) = (p(x,t),~ u(x,t))^T

and the coefficient matrix is 

.. math:: A = \left[\begin{array}{cc} 0&K\\ 1/\rho & 0\end{array}\right].
         
The density rho and bulk modulus K are set in `setrun.py` and then written out
to `setprob.data`, which is read in by the Fortran code.

