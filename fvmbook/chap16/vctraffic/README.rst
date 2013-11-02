
.. _fvmbook_chap16:

Variable-Coefficient Traffic Flow Model
------------------------------------------

    
Example [book/chap16/vctraffic] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.

Variable-coefficient traffic flow model.  The flux function is
.. math::  f(q,x) = u(x)*q*(1-q)
where the "speed limit" :math:`u(x)` varies with x. 
It's value in cell i is stored in aux(i,1) (see setaux.f).

Here a Riemann problem is solved with 

   :math:`u(x) = 2` for :math:`x<0`

   :math:`u(x) = 1` for :math:`x>0`

The initial data is set in qinit.f.   
Set ql to 0.13 for Figure 16.9
Set ql to 0.2 for Figure 16.10

After running this code and creating plots via "make .plots", you should be
able to view the plots in _PlotIndex.html.
        

