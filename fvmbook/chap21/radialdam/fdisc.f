c
c
c
c     =================================================
      function fdisc(x,y)
c     =================================================

      implicit double precision (a-h,o-z)
      
      ! location of dam:
      real(kind=8) :: r0
      common /cdisc/ r0
c
c     # For computing cell averages for initial data or coefficients that
c     # have a discontinuity along some curve.  

c     # fdisc should be negative to the "left" of the curve and 
c     # positive to the "right".

c     # The cellave routine can then be used to compute the fraction wl of
c     # a grid cell that lies to the "left" of the curve.

c     # Here the curve is the circle with radius r0:

      fdisc = x**2 + y**2 - r0**2
c
      return
      end
