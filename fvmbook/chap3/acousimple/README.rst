
.. _fvmbook_chapX_XX:

TitleXX
------------------------------------------

    
Example [book/chap3/acousimple]
to accompany Figure 3.1 of the book 
`Finite Volume Methods for Hyperbolic Problems <http://www.clawpack.org/book>`_
by R. J. LeVeque.

Converted to Clawpack 5.0 form in 2013.
        

1d acoustics in a constant medium.
          :math:`q_t + A q_x = 0`
where
          :math:`q(x,t) = \vector{ p(x,t)\\ u(x,t)}`
and the coefficient matrix is
          :math:`A = \begin{matrix}
                        0         & K\\
                        1/\rho & 0
                        \end{matrix}.`
         


