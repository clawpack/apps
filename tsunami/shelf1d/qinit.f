c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c     # Pulse in h, zero velocity
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
      common /comeps/ eps
      common /comrp/ grav
      
      pi = 4.d0*datan(1.d0)
c
c
c
       do 150 i=1,mx
         xcell = xlower + (i-0.5d0)*dx
         q(1,i) = 0.d0 - aux(1,i)
         q(2,i) = 0.d0
         c = dsqrt(grav*q(1,i))
c        x1 = -2000.e3
c        x2 = -2000.e3
         x1 = -180.e3
         x2 = -130.e3
         x3 = -80.e3
         xmid = 0.5d0*(x1+x3)

         if (.false.) then
         if (xcell.gt.x1 .and. xcell.lt.x2) then
            q(1,i) = q(1,i) - eps
            q(2,i) = -eps*c
         else if (xcell.gt.x2 .and. xcell.lt.x3) then
            q(1,i) = q(1,i) + eps
            q(2,i) = eps*c
         endif
         endif

c        if (xcell.gt.x1 .and. xcell.lt.x3) then
         if (xcell.gt.x2 .and. xcell.lt.x3) then
            deta =  eps*dsin((xcell-xmid)*pi/(x3-xmid))
            q(1,i) = q(1,i) + deta
c           q(2,i) = c*deta
            q(2,i) = 0.d0
         endif
         

  150    continue
c
      return
      end

