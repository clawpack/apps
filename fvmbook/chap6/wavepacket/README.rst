
.. _fvmbook_chap6/wavepacket:

Advection with wave packet data
--------------------------------------------------

    
Example [book/chap6/wavepacket] to accompany the book 
`Finite Volume Methods for Hyperbolic Problems
<http://www.clawpack.org/book.html>`_
by R. J. LeVeque.


Advection with wavepacket initial data.  

**Note:**

 - Periodic boundary conditions are used on a domain of length 1 with
   advection velocity u=1.

 - The output is set to integer times so the pulse should have propagated
   one period each frame.
        
 - Try changing `clawdata.limiter` in `setrun.py` to test each limiter.

 - Set `clawdata.order = 1` for the upwind method.


**Revision history:**

 - Converted to Clawpack 5.0 form in 2013.
 - Updated for Clawpack 5.4.0 in January, 2017
