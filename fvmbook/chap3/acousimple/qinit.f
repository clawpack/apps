c
c
c =========================================================
       subroutine qinit(maxmx,meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c     # Pulse in pressure, zero velocity
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:maxmx+mbc)
      dimension aux(maux,1-mbc:maxmx+mbc)
      common /cqinit/ beta
c
c
      do 150 i=1,mx
	 xcell = xlower + (i-0.5d0)*dx
	 q(1,i) = 0.5d0*dexp(-80.d0*xcell**2)
	 if (dabs(xcell+0.2d0) .lt. 0.1d0)  then
	    q(1,i) = q(1,i) + 0.5d0
	    endif
	 q(2,i) = 0.d0
  150    continue
c
      return
      end



