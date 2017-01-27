
.. _fvmbook_chap7/advinflow:

Advection with inflow boundary conditions.
------------------------------------------

Inflow boundary condition :math:`u(0,t) = g(t)` at :math:`x=0`
are specified by the user in the routines `g.f` and
`bc1.f` by setting the ghost cells at the left edge to:

:math:`Q_0^n = g(t + \Delta x/2u)`

:math:`Q_{-1}^n = g(t + 3\Delta x/2u)`


    
Example [book/chap7/advinflow] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.
        

