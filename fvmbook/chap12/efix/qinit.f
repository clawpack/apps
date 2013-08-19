c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
c
c
      ql = -1.d0
      qr =  2.d0

      do 150 i=1,mx
c        # left and right edge of i'th cell:
         xl = xlower + (i-1)*dx
         xr = xl+dx

         if (xl .ge. 0.d0) then
             q(1,i) = qr
           else if (xr .le. 0.d0) then
             q(1,i) = ql
           else
c            #  xl < 0 < xr and the cell average is weighted combo of ql,qr:
             q(1,i) = (-xl*ql + xr*qr) / dx
           endif
  150    continue
c
      return
      end

