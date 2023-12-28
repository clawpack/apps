.. _fvmbook_chap21_radialdam:

Shallow water equations with radial dam break data
--------------------------------------------------


Example [book/chap21/radialdam] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems <http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2023.
        

Shallow water equations with radial symmetric initial conditions.  
The solution should remain radially symmetric.  

First run the code in the 1drad subdirectory to
compute the "reference solution" and then setplot.py contains code to produce a
scatter plot of the computed depth h vs. distance from origin compared
with the 1d solution.

