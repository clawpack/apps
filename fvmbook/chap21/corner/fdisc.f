c
c
c
c     =================================================
      function fdisc(x,y)
c     =================================================

      implicit double precision (a-h,o-z)
      
c
c     # For computing cell averages for initial data or coefficients that
c     # have a discontinuity along some curve.  

c     # fdisc should be negative to the "left" of the curve and 
c     # positive to the "right".

c     # The cellave routine can then be used to compute the fraction wl of
c     # a grid cell that lies to the "left" of the curve.

c     # half wedge:

      if (x .gt. 0.d0 .and. (y.lt.(0.55d0*x))) then
          fdisc = 1.d0
      else
          fdisc = -1.d0
      endif
c
      return
      end
