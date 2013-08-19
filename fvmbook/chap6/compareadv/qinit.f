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
      common /comic/ beta
c
c
      pi2 = 8.d0*datan(1.d0)  !# = 2 * pi
      do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx
         q(1,i) = dexp(-beta * (xcell-0.3d0)**2)
         if (xcell.gt.0.6d0 .and. xcell.lt.0.8d0) then
             q(1,i) = q(1,i) + 1.d0
             endif
  150    continue
c
      return
      end

