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
      common/cdisc/ x0,y0,alf,beta,r0,idisc
      common /comic/ hin,hout
c
      pi = 4.d0*datan(1.d0)
      width = 0.2d0
c
      write(6,*) '+++ mx = ',mx
      do 150 i=1,mx
	     xcell = xlower + (i-0.5d0)*dx
	     if (xcell .lt. r0) then
             h = hin
           else
             h = hout
           endif
         q(1,i) = h
         q(2,i) = 0.d0
  150    continue
c
      return
      end

